from django.shortcuts import render, redirect
from django.db import connection


def studio_list(request):

    with connection.cursor() as cursor:

        cursor.execute("""

        SELECT
            S.STUDIO_ID,
            S.STUDIO_NAME,
            S.LOCATION,
            S.CAPACITY,
            S.STUDIO_TYPE,
            S.EQUIPMENT,
            S.STATUS,
            T.TOOL_NAME

        FROM STUDIO S

        LEFT JOIN TOOL T
        ON S.STUDIO_ID = T.STUDIO_ID

        ORDER BY S.STUDIO_ID

        """)

        studios = cursor.fetchall()

    return render(request,
                  'studio_list.html',
                  {'studios': studios})


def add_studio(request):

    if request.method == 'POST':

        studio_id = request.POST.get('studio_id')
        studio_name = request.POST.get('studio_name')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity')
        studio_type = request.POST.get('studio_type')
        equipment = request.POST.get('equipment')

        with connection.cursor() as cursor:

            cursor.execute("""

            INSERT INTO STUDIO
            (
                STUDIO_ID,
                STUDIO_NAME,
                LOCATION,
                CAPACITY,
                STUDIO_TYPE,
                EQUIPMENT,
                STATUS
            )

            VALUES (%s, %s, %s, %s, %s, %s, %s)

            """, [
                studio_id,
                studio_name,
                location,
                capacity,
                studio_type,
                equipment,
                'Active'
            ])

        return redirect('studio_list')

    return render(request, 'add_studio.html')


def deactivate_studio(request, studio_id):

    with connection.cursor() as cursor:

        cursor.execute("""

        UPDATE STUDIO
        SET STATUS = 'Inactive'
        WHERE STUDIO_ID = %s

        """, [studio_id])

    return redirect('studio_list')