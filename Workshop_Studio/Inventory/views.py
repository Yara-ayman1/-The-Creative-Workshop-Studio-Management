from django.shortcuts import render, redirect
from django.db import connection

def _fetch_studios():
    with connection.cursor() as cursor:
        cursor.execute("SELECT STUDIO_ID, STUDIO_NAME FROM STUDIO ORDER BY STUDIO_NAME")
        return cursor.fetchall()

def inventory_dashboard(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT rm.MATERIAL_ID, rm.MAT_NAME, rm.UNIT, rm.QUANTITY_IN_STOCK, rm.CATEGORY, s.STUDIO_NAME
            FROM RAW_MATERIAL rm
            LEFT JOIN STUDIO s ON s.STUDIO_ID = rm.STUDIO_ID
        """)
        materials = cursor.fetchall()
        studios = _fetch_studios()

    return render(request, 'Inventory.html', {'materials': materials, 'studios': studios})

def add_material(request):
    if request.method == 'POST':

        mat_id = request.POST.get('material_id')
        name = request.POST.get('name')
        unit = request.POST.get('unit')
        qty = int(request.POST.get('quantity'))
        cat = request.POST.get('category')
        studio_id = request.POST.get('studio_id')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO RAW_MATERIAL
                (MATERIAL_ID, MAT_NAME, UNIT, QUANTITY_IN_STOCK, CATEGORY, STUDIO_ID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [mat_id, name, unit, qty, cat, studio_id])

    return redirect('inventory_dashboard')

def record_consumption(request):
    if request.method == 'POST':

        mat_id = request.POST.get('mat_id')
        amount = int(request.POST.get('amount'))

        with connection.cursor() as cursor:

            cursor.execute("""
                UPDATE RAW_MATERIAL
                SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK - %s
                WHERE MATERIAL_ID = %s AND QUANTITY_IN_STOCK >= %s
            """, [amount, mat_id, amount])

    return redirect('inventory_dashboard')

def increase_stock(request):
    if request.method == 'POST':

        mat_id = request.POST.get('mat_id')
        amount = int(request.POST.get('amount'))

        with connection.cursor() as cursor:

            cursor.execute("""
                UPDATE RAW_MATERIAL
                SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK + %s
                WHERE MATERIAL_ID = %s
            """, [amount, mat_id])

    return redirect('inventory_dashboard')

def delete_material(request):
    if request.method == 'POST':

        mat_id = request.POST.get('mat_id')

        with connection.cursor() as cursor:

            cursor.execute("""
                DELETE FROM RAW_MATERIAL
                WHERE MATERIAL_ID = %s
            """, [mat_id])

    return redirect('inventory_dashboard')