from django.shortcuts import render, redirect
from django.db import connection


# =========================
# DASHBOARD
# =========================
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

    return render(request, 'studio_dashboard.html', {'studios': studios})


# =========================
# ADD STUDIO
# =========================
def add_studio(request):

    if request.method == 'POST':

        with connection.cursor() as cursor:

            cursor.execute("""
                INSERT INTO STUDIO (
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
                request.POST.get('studio_id'),
                request.POST.get('studio_name'),
                request.POST.get('location'),
                request.POST.get('capacity'),
                request.POST.get('studio_type'),
                request.POST.get('equipment'),
                'Active'
            ])

        return redirect('studio_list')

    return render(request, 'add_studio.html')


# =========================
# EDIT STUDIO
# =========================
def edit_studio(request, studio_id):

    if request.method == 'POST':

        with connection.cursor() as cursor:

            cursor.execute("""
                UPDATE STUDIO
                SET
                    STUDIO_NAME = %s,
                    LOCATION = %s,
                    CAPACITY = %s,
                    STUDIO_TYPE = %s,
                    EQUIPMENT = %s
                WHERE STUDIO_ID = %s
            """, [
                request.POST.get('studio_name'),
                request.POST.get('location'),
                request.POST.get('capacity'),
                request.POST.get('studio_type'),
                request.POST.get('equipment'),
                studio_id
            ])

        return redirect('studio_list')

    else:

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    STUDIO_ID,
                    STUDIO_NAME,
                    LOCATION,
                    CAPACITY,
                    STUDIO_TYPE,
                    EQUIPMENT,
                    STATUS
                FROM STUDIO
                WHERE STUDIO_ID = %s
            """, [studio_id])

            studio = cursor.fetchone()

        return render(request, 'edit_studio.html', {'studio': studio})


# =========================
# DELETE STUDIO
# =========================
def delete_studio(request, studio_id):

    if request.method == 'POST':

        with connection.cursor() as cursor:

            cursor.execute("""
                DELETE FROM STUDIO
                WHERE STUDIO_ID = %s
            """, [studio_id])

    return redirect('studio_list')
# =====================================
# DEACTIVATE STUDIO
# =====================================
def deactivate_studio(request, studio_id):

    with connection.cursor() as cursor:

        cursor.execute("""

            UPDATE STUDIO

            SET STATUS = 'Inactive'

            WHERE STUDIO_ID = %s

        """, [studio_id])

    return redirect('studio_list')
