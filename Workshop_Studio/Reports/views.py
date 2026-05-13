from django.shortcuts import render
from django.db import connection
from datetime import datetime, timedelta

def reports_dashboard(request):
    # Calculate last month's range
    today = datetime.now()
    # If today is May 13 2026, last month is April 2026
    # first_day_this_month = today.replace(day=1)
    # last_day_last_month = first_day_this_month - timedelta(days=1)
    # first_day_last_month = last_day_last_month.replace(day=1)
    
    # Actually, let's use SQL's DATEADD for better consistency with the database's idea of "last month"
    # but we need period_start/end for display.
    with connection.cursor() as cursor:
        cursor.execute("SELECT CONVERT(varchar, DATEADD(month, DATEDIFF(month, 0, GETDATE()) - 1, 0), 23)")
        period_start = cursor.fetchone()[0]
        cursor.execute("SELECT CONVERT(varchar, DATEADD(day, -1, DATEADD(month, DATEDIFF(month, 0, GETDATE()), 0)), 23)")
        period_end = cursor.fetchone()[0]

    with connection.cursor() as cursor:
        # 1. Which workshop had the maximum number of participants last month?
        # Expected q1: (title, craft_type, count, instructor, studio, date)
        cursor.execute("""
            SELECT TOP 1 
                w.TITLE, w.CRAFT_TYPE, COUNT(r.MEMBER_ID) as participant_count,
                ra.FIRST_NAME + ' ' + ra.LAST_NAME as instructor,
                s.STUDIO_NAME,
                CONVERT(varchar, w.WORKSHOP_DATE, 23) as workshop_date
            FROM WORKSHOP w
            LEFT JOIN REGISTERS r ON w.ARTIST_ID = r.ARTIST_ID AND w.STUDIO_ID = r.STUDIO_ID AND w.WORKSHOP_ID = r.WORKSHOP_ID
            JOIN RESIDENT_ARTIST ra ON w.ARTIST_ID = ra.ARTIST_ID
            JOIN STUDIO s ON w.STUDIO_ID = s.STUDIO_ID
            WHERE w.WORKSHOP_DATE BETWEEN %s AND %s
            GROUP BY w.ARTIST_ID, w.STUDIO_ID, w.WORKSHOP_ID, w.TITLE, w.CRAFT_TYPE, ra.FIRST_NAME, ra.LAST_NAME, s.STUDIO_NAME, w.WORKSHOP_DATE
            ORDER BY participant_count DESC
        """, [period_start, period_end])
        q1 = cursor.fetchone()

        # 2. Which studio had no bookings or workshops held in it last month?
        # Expected q2: (studio_id, studio_name, studio_type, location)
        cursor.execute("""
            SELECT STUDIO_ID, STUDIO_NAME, STUDIO_TYPE, LOCATION
            FROM STUDIO
            WHERE STUDIO_ID NOT IN (
                SELECT DISTINCT STUDIO_ID 
                FROM WORKSHOP 
                WHERE WORKSHOP_DATE BETWEEN %s AND %s
            )
            AND STUDIO_ID NOT IN (
                SELECT DISTINCT STUDIO_ID 
                FROM BOOKS 
                WHERE BOOKING_DATE BETWEEN %s AND %s
            )
        """, [period_start, period_end, period_start, period_end])
        q2 = cursor.fetchall()

        # 3. Who was the resident artist who taught the highest number of workshops last month?
        # Expected q3: (artist_id, name, specialty, count)
        cursor.execute("""
            SELECT TOP 1 
                ra.ARTIST_ID, ra.FIRST_NAME + ' ' + ra.LAST_NAME as name, ra.SPECIALTY,
                COUNT(w.WORKSHOP_ID) as workshop_count
            FROM RESIDENT_ARTIST ra
            JOIN WORKSHOP w ON ra.ARTIST_ID = w.ARTIST_ID
            WHERE w.WORKSHOP_DATE BETWEEN %s AND %s
            GROUP BY ra.ARTIST_ID, ra.FIRST_NAME, ra.LAST_NAME, ra.SPECIALTY
            ORDER BY workshop_count DESC
        """, [period_start, period_end])
        q3 = cursor.fetchone()

        # 4. Identify members who did not rent any tools or join any workshops last month.
        # Expected q4: (member_id, name, email, membership_type)
        cursor.execute("""
            SELECT MEMBER_ID, FIRST_NAME + ' ' + LAST_NAME as name, EMAIL, MEMBERSHIP_TYPE
            FROM MEMBER
            WHERE MEMBER_ID NOT IN (
                SELECT DISTINCT MEMBER_ID 
                FROM RENTS 
                WHERE PICKUP_TIME BETWEEN %s AND %s
            )
            AND MEMBER_ID NOT IN (
                SELECT DISTINCT MEMBER_ID 
                FROM REGISTERS 
                WHERE REG_DATE BETWEEN %s AND %s
            )
        """, [period_start, period_end, period_start, period_end])
        q4 = cursor.fetchall()

        # 5. What were the raw materials consumed by each workshop held last month?
        # Expected q5: {(title, craft_type, date): [(name, unit, qty), ...]}
        cursor.execute("""
            SELECT 
                w.TITLE, w.CRAFT_TYPE, CONVERT(varchar, w.WORKSHOP_DATE, 23) as workshop_date,
                rm.MAT_NAME, rm.UNIT, c.QTY_USED
            FROM WORKSHOP w
            JOIN CONSUMES c ON w.ARTIST_ID = c.ARTIST_ID AND w.STUDIO_ID = c.STUDIO_ID AND w.WORKSHOP_ID = c.WORKSHOP_ID
            JOIN RAW_MATERIAL rm ON c.MATERIAL_ID = rm.MATERIAL_ID
            WHERE w.WORKSHOP_DATE BETWEEN %s AND %s
            ORDER BY w.WORKSHOP_DATE, w.TITLE
        """, [period_start, period_end])
        q5_raw = cursor.fetchall()
        
        q5 = {}
        for row in q5_raw:
            key = (row[0], row[1], row[2])
            if key not in q5:
                q5[key] = []
            q5[key].append((row[3], row[4], row[5]))

        # 6. For each tool, retrieve its description and the total number of times it was rented.
        # Expected q6: (tool_id, tool_name, description, total_rentals)
        cursor.execute("""
            SELECT 
                TOOL_ID, TOOL_NAME, DESCRIPTION, TOTAL_RENTALS
            FROM TOOL
        """)
        q6 = cursor.fetchall()

    context = {
        'period_start': period_start,
        'period_end': period_end,
        'q1': q1,
        'q2': q2,
        'q3': q3,
        'q4': q4,
        'q5': q5,
        'q6': q6,
    }
    return render(request, 'report_dashborad.html', context)
