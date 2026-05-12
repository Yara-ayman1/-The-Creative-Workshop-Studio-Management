# views.py

from django.shortcuts import render, redirect
from django.db import connection
from datetime import datetime

def tool_dashboard(request):

    with connection.cursor() as cursor:

        cursor.execute("""

            SELECT 
                TOOL.TOOL_ID,
                TOOL.STUDIO_ID,
                TOOL.TOOL_NAME,
                TOOL.DESCRIPTION,
                TOOL.TOOL_CONDITION,
                TOOL.TOTAL_RENTALS,

                RENTS.MEMBER_ID,
                RENTS.PICKUP_TIME,
                RENTS.RETURN_TIME

            FROM TOOL

            LEFT JOIN RENTS
            ON TOOL.TOOL_ID = RENTS.TOOL_ID

        """)

        tools = cursor.fetchall()

    return render(request, 'Tools.html', {'tools': tools})

def rent_tool(request):

    if request.method == 'POST':

        tool_id = request.POST.get('tool_id')
        member_id = request.POST.get('member_id')
        pickup_time = request.POST.get('pickup_time')
        return_time = request.POST.get('return_time')
        condition = request.POST.get('condition')

        pickup_time = datetime.strptime(
            pickup_time,
            "%Y-%m-%dT%H:%M"
        )
        return_time = datetime.strptime(
            return_time,
            "%Y-%m-%dT%H:%M"
        )
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT *
                FROM RENTS
                WHERE TOOL_ID = %s
            """, [tool_id])

            exists = cursor.fetchone()
            if exists:
                cursor.execute("""

                    UPDATE RENTS
                    SET MEMBER_ID = %s,
                        PICKUP_TIME = %s,
                        RETURN_TIME = %s
                    WHERE TOOL_ID = %s
                """, [
                    member_id,
                    pickup_time,
                    return_time,
                    tool_id
                ])
            else:
                cursor.execute("""

                    INSERT INTO RENTS
                    (
                        TOOL_ID,
                        MEMBER_ID,
                        PICKUP_TIME,
                        RETURN_TIME
                    )
                    VALUES (%s, %s, %s, %s)
                """, [
                    tool_id,
                    member_id,
                    pickup_time,
                    return_time
                ])
            cursor.execute("""
                UPDATE TOOL
                SET TOOL_CONDITION = %s,
                    TOTAL_RENTALS = TOTAL_RENTALS + 1
                WHERE TOOL_ID = %s
            """, [
                condition,
                tool_id
            ])

    return redirect('tool_dashboard')

def return_tool(request):

    if request.method == 'POST':

        tool_id = request.POST.get('tool_id')
        condition = request.POST.get('condition')

        with connection.cursor() as cursor:

            cursor.execute("""

                DELETE FROM RENTS
                WHERE TOOL_ID = %s

            """, [tool_id])

            cursor.execute("""

                UPDATE TOOL
                SET TOOL_CONDITION = %s
                WHERE TOOL_ID = %s

            """, [condition, tool_id])

    return redirect('tool_dashboard')

def add_tool(request):

    if request.method == 'POST':
        
        tool_id = request.POST.get('tool_id')
        tool_name = request.POST.get('tool_name')
        description = request.POST.get('description')
        condition = request.POST.get('condition')
        studio_id = request.POST.get('studio_id')

        with connection.cursor() as cursor:

            cursor.execute("""

                INSERT INTO TOOL
                (TOOL_ID, TOOL_NAME, DESCRIPTION, TOOL_CONDITION, TOTAL_RENTALS)

                VALUES (%s, %s, %s, %s, %s)

            """, [
                tool_id,
                tool_name,
                description,
                condition,
                0
            ])

    return redirect('tool_dashboard')

def delete_tool(request):

    if request.method == 'POST':

        tool_id = request.POST.get('tool_id')

        with connection.cursor() as cursor:

            cursor.execute("""
                DELETE FROM RENTS
                WHERE TOOL_ID = %s
            """, [tool_id])

            cursor.execute("""
                DELETE FROM TOOL
                WHERE TOOL_ID = %s
            """, [tool_id])

    return redirect('tool_dashboard')    