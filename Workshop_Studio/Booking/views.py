from django.shortcuts import render
from django.db import connection
from datetime import datetime


def book_studio(request):

    error_message = None
    success_message = None

    if request.method == 'POST':

        studio_id = request.POST.get('studio_id')
        member_id = request.POST.get('member_id')
        booking_date = request.POST.get('booking_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        start_datetime = datetime.strptime(
            f"{booking_date} {start_time}",
            "%Y-%m-%d %H:%M"
        )

        end_datetime = datetime.strptime(
            f"{booking_date} {end_time}",
            "%Y-%m-%d %H:%M"
        )

        with connection.cursor() as cursor:

            # 1) Check member
            cursor.execute("""
                SELECT *
                FROM MEMBER
                WHERE MEMBER_ID = %s
                AND MEMBERSHIP_END >= GETDATE()
            """, [member_id])

            if not cursor.fetchone():
                error_message = "Membership expired"

            # 2) Check capacity
            if not error_message:

                cursor.execute("""
                    SELECT CAPACITY
                    FROM STUDIO
                    WHERE STUDIO_ID = %s
                """, [studio_id])

                capacity = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM BOOKS
                    WHERE STUDIO_ID = %s
                    AND BOOKING_DATE = %s
                """, [studio_id, booking_date])

                current = cursor.fetchone()[0]

                if current >= capacity:
                    error_message = "Studio is full"

            # 3) Check time conflict
            if not error_message:

                cursor.execute("""
                    SELECT *
                    FROM BOOKS
                    WHERE STUDIO_ID = %s
                    AND BOOKING_DATE = %s
                    AND (START_TIME < %s AND END_TIME > %s)
                """, [
                    studio_id,
                    booking_date,
                    end_datetime,
                    start_datetime
                ])

                if cursor.fetchone():
                    error_message = "Time slot already booked"

            # 4) Insert booking if no error
            if not error_message:

                cursor.execute("""
                    INSERT INTO BOOKS
                    (STUDIO_ID, MEMBER_ID, BOOKING_DATE, START_TIME, END_TIME)
                    VALUES (%s, %s, %s, %s, %s)
                """, [
                    studio_id,
                    member_id,
                    booking_date,
                    start_datetime,
                    end_datetime
                ])

                success_message = "Booking successful "

    # GET studios
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT STUDIO_ID, STUDIO_NAME
            FROM STUDIO
            WHERE STATUS = 'Active'
        """)
        studios = cursor.fetchall()

    return render(request, 'book_studio.html', {
        'studios': studios,
        'error_message': error_message,
        'success_message': success_message
    })
