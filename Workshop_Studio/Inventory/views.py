from django.shortcuts import render, redirect
from django.db import connection


def inventory_dashboard(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT MATERIAL_ID, MAT_NAME, UNIT, QUANTITY_IN_STOCK, CATEGORY
            FROM RAW_MATERIAL
        """)
        materials = cursor.fetchall()

    return render(request, 'Inventory.html', {'materials': materials})

def add_material(request):
    if request.method == 'POST':

        mat_id = request.POST.get('material_id')
        name = request.POST.get('name')
        unit = request.POST.get('unit')
        qty = int(request.POST.get('quantity'))
        cat = request.POST.get('category')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO RAW_MATERIAL
                (MATERIAL_ID, MAT_NAME, UNIT, QUANTITY_IN_STOCK, CATEGORY)
                VALUES (%s, %s, %s, %s, %s)
            """, [mat_id, name, unit, qty, cat])

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