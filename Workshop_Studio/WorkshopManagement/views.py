from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from datetime import datetime




def _fetch_studios():
    with connection.cursor() as cursor:
        cursor.execute("SELECT STUDIO_ID, STUDIO_NAME FROM STUDIO ORDER BY STUDIO_NAME")
        return cursor.fetchall()

def _fetch_artists():
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT ARTIST_ID, FIRST_NAME, LAST_NAME, SPECIALTY FROM RESIDENT_ARTIST ORDER BY FIRST_NAME"
        )
        return cursor.fetchall()

def _next_workshop_id(artist_id, studio_id):
    """Return the next available WORKSHOP_ID for a given (artist, studio) pair."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT ISNULL(MAX(WORKSHOP_ID), 0) + 1
            FROM WORKSHOP
            WHERE ARTIST_ID = %s AND STUDIO_ID = %s
            """,
            [artist_id, studio_id],
        )
        return cursor.fetchone()[0]




def workshop_list(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                w.ARTIST_ID, w.STUDIO_ID, w.WORKSHOP_ID,
                w.TITLE, w.CRAFT_TYPE,
                CONVERT(varchar, w.WORKSHOP_DATE, 23)  AS WORKSHOP_DATE,
                CONVERT(varchar, w.START_TIME,    108) AS START_TIME,
                CONVERT(varchar, w.END_TIME,      108) AS END_TIME,
                w.MAX_PARTICIPANTS,
                ra.FIRST_NAME + ' ' + ra.LAST_NAME     AS ARTIST_NAME,
                s.STUDIO_NAME
            FROM WORKSHOP w
            JOIN RESIDENT_ARTIST ra ON ra.ARTIST_ID = w.ARTIST_ID
            JOIN STUDIO           s  ON  s.STUDIO_ID = w.STUDIO_ID
            ORDER BY w.WORKSHOP_DATE DESC, w.START_TIME
            """
        )
        workshops = cursor.fetchall()

    return render(request, 'workshop_list.html', {'workshops': workshops})



def add_workshop(request):
    studios = _fetch_studios()
    artists = _fetch_artists()
    error   = None

    if request.method == 'POST':
        artist_id        = request.POST.get('artist_id')
        studio_id        = request.POST.get('studio_id')
        title            = request.POST.get('title')
        craft_type       = request.POST.get('craft_type')
        workshop_date    = request.POST.get('workshop_date')
        start_time       = request.POST.get('start_time')
        end_time         = request.POST.get('end_time')
        max_participants = request.POST.get('max_participants')

        if not all([artist_id, studio_id, title, craft_type, workshop_date,
                    start_time, end_time, max_participants]):
            error = "All fields are required."
        else:
            workshop_id = _next_workshop_id(artist_id, studio_id)
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO WORKSHOP
                        (ARTIST_ID, STUDIO_ID, WORKSHOP_ID,
                         TITLE, CRAFT_TYPE, WORKSHOP_DATE,
                         START_TIME, END_TIME, MAX_PARTICIPANTS)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [
                        artist_id, studio_id, workshop_id,
                        title, craft_type, workshop_date,
                        f"{workshop_date} {start_time}",
                        f"{workshop_date} {end_time}",
                        max_participants,
                    ],
                )
            return redirect('workshop_list')

    return render(request, 'add_workshop.html',
                  {'studios': studios, 'artists': artists, 'error': error})




def edit_workshop(request, artist_id, studio_id, workshop_id):
    studios = _fetch_studios()
    artists = _fetch_artists()
    error   = None

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                ARTIST_ID, STUDIO_ID, WORKSHOP_ID,
                TITLE, CRAFT_TYPE,
                CONVERT(varchar, WORKSHOP_DATE, 23)  AS WORKSHOP_DATE,
                CONVERT(varchar, START_TIME,    108) AS START_TIME,
                CONVERT(varchar, END_TIME,      108) AS END_TIME,
                MAX_PARTICIPANTS
            FROM WORKSHOP
            WHERE ARTIST_ID = %s AND STUDIO_ID = %s AND WORKSHOP_ID = %s
            """,
            [artist_id, studio_id, workshop_id],
        )
        workshop = cursor.fetchone()

    if not workshop:
        return redirect('workshop_list')

    if request.method == 'POST':
        title            = request.POST.get('title')
        craft_type       = request.POST.get('craft_type')
        workshop_date    = request.POST.get('workshop_date')
        start_time       = request.POST.get('start_time')
        end_time         = request.POST.get('end_time')
        max_participants = request.POST.get('max_participants')

        if not all([title, craft_type, workshop_date, start_time, end_time, max_participants]):
            error = "All fields are required."
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE WORKSHOP
                    SET TITLE            = %s,
                        CRAFT_TYPE       = %s,
                        WORKSHOP_DATE    = %s,
                        START_TIME       = %s,
                        END_TIME         = %s,
                        MAX_PARTICIPANTS = %s
                    WHERE ARTIST_ID = %s AND STUDIO_ID = %s AND WORKSHOP_ID = %s
                    """,
                    [
                        title, craft_type, workshop_date,
                        f"{workshop_date} {start_time}",
                        f"{workshop_date} {end_time}",
                        max_participants,
                        artist_id, studio_id, workshop_id,
                    ],
                )
            return redirect('workshop_list')

    return render(request, 'edit_workshop.html',
                  {'workshop': workshop, 'studios': studios,
                   'artists': artists, 'error': error})



def delete_workshop(request, artist_id, studio_id, workshop_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            # Remove child rows first to respect FK constraints
            cursor.execute(
                """
                DELETE FROM CONSUMES
                WHERE ARTIST_ID = %s AND STUDIO_ID = %s AND WORKSHOP_ID = %s
                """,
                [artist_id, studio_id, workshop_id],
            )
            cursor.execute(
                """
                DELETE FROM REGISTERS
                WHERE ARTIST_ID = %s AND STUDIO_ID = %s AND WORKSHOP_ID = %s
                """,
                [artist_id, studio_id, workshop_id],
            )
            cursor.execute(
                """
                DELETE FROM WORKSHOP
                WHERE ARTIST_ID = %s AND STUDIO_ID = %s AND WORKSHOP_ID = %s
                """,
                [artist_id, studio_id, workshop_id],
            )
    return redirect('workshop_list')




def workshop_detail(request, artist_id, studio_id, workshop_id):
    with connection.cursor() as cursor:
        # Workshop header
        cursor.execute(
            """
            SELECT
                w.TITLE, w.CRAFT_TYPE,
                CONVERT(varchar, w.WORKSHOP_DATE, 23)  AS WORKSHOP_DATE,
                CONVERT(varchar, w.START_TIME,    108) AS START_TIME,
                CONVERT(varchar, w.END_TIME,      108) AS END_TIME,
                w.MAX_PARTICIPANTS,
                ra.FIRST_NAME + ' ' + ra.LAST_NAME AS ARTIST_NAME,
                s.STUDIO_NAME
            FROM WORKSHOP w
            JOIN RESIDENT_ARTIST ra ON ra.ARTIST_ID = w.ARTIST_ID
            JOIN STUDIO           s  ON  s.STUDIO_ID = w.STUDIO_ID
            WHERE w.ARTIST_ID = %s AND w.STUDIO_ID = %s AND w.WORKSHOP_ID = %s
            """,
            [artist_id, studio_id, workshop_id],
        )
        workshop = cursor.fetchone()

        # Registered members
        cursor.execute(
            """
            SELECT m.MEMBER_ID,
                   m.FIRST_NAME + ' ' + m.LAST_NAME AS MEMBER_NAME,
                   m.EMAIL,
                   CONVERT(varchar, r.REG_DATE, 23) AS REG_DATE
            FROM REGISTERS r
            JOIN MEMBER m ON m.MEMBER_ID = r.MEMBER_ID
            WHERE r.ARTIST_ID = %s AND r.STUDIO_ID = %s AND r.WORKSHOP_ID = %s
            ORDER BY r.REG_DATE
            """,
            [artist_id, studio_id, workshop_id],
        )
        registrations = cursor.fetchall()

        # Materials consumed
        cursor.execute(
            """
            SELECT rm.MAT_NAME, rm.UNIT, c.QTY_USED, c.MATERIAL_ID
            FROM CONSUMES c
            JOIN RAW_MATERIAL rm ON rm.MATERIAL_ID = c.MATERIAL_ID
            WHERE c.ARTIST_ID = %s AND c.STUDIO_ID = %s AND c.WORKSHOP_ID = %s
            """,
            [artist_id, studio_id, workshop_id],
        )
        materials = cursor.fetchall()

        # All members (for registration dropdown)
        cursor.execute("SELECT MEMBER_ID, FIRST_NAME + ' ' + LAST_NAME FROM MEMBER ORDER BY FIRST_NAME")
        all_members = cursor.fetchall()

        # All raw materials (for consumption dropdown)
        cursor.execute("SELECT MATERIAL_ID, MAT_NAME, UNIT, QUANTITY_IN_STOCK FROM RAW_MATERIAL ORDER BY MAT_NAME")
        all_materials = cursor.fetchall()

    return render(request, 'workshop_detail.html', {
        'workshop':      workshop,
        'registrations': registrations,
        'materials':     materials,
        'all_members':   all_members,
        'all_materials': all_materials,
        'artist_id':     artist_id,
        'studio_id':     studio_id,
        'workshop_id':   workshop_id,
    })




def register_member(request, artist_id, studio_id, workshop_id):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        reg_date  = request.POST.get('reg_date')

        with connection.cursor() as cursor:
            # Check if workshop has ended
            cursor.execute(
                """
                SELECT END_TIME, TITLE FROM WORKSHOP
                WHERE ARTIST_ID = %s AND STUDIO_ID = %s AND WORKSHOP_ID = %s
                """,
                [artist_id, studio_id, workshop_id],
            )
            row = cursor.fetchone()
            if not row:
                messages.error(request, "Workshop not found.")
                return redirect('workshop_detail', artist_id=artist_id, studio_id=studio_id, workshop_id=workshop_id)
            
            end_time = row[0]
            if end_time < datetime.now():
                messages.error(request, f"Cannot register for '{row[1]}' because it has already ended.")
                return redirect('workshop_detail', artist_id=artist_id, studio_id=studio_id, workshop_id=workshop_id)

            # Check capacity
            cursor.execute(
                """
                SELECT MAX_PARTICIPANTS FROM WORKSHOP
                WHERE ARTIST_ID = %s AND STUDIO_ID = %s AND WORKSHOP_ID = %s
                """,
                [artist_id, studio_id, workshop_id],
            )
            max_p = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*) FROM REGISTERS
                WHERE ARTIST_ID = %s AND STUDIO_ID = %s AND WORKSHOP_ID = %s
                """,
                [artist_id, studio_id, workshop_id],
            )
            current = cursor.fetchone()[0]

            if current >= max_p:
                messages.error(request, "Workshop is at full capacity.")
                return redirect('workshop_detail',
                                artist_id=artist_id, studio_id=studio_id,
                                workshop_id=workshop_id)

            # Avoid duplicate registration
            cursor.execute(
                """
                SELECT 1 FROM REGISTERS
                WHERE MEMBER_ID = %s AND ARTIST_ID = %s
                  AND STUDIO_ID = %s AND WORKSHOP_ID = %s
                """,
                [member_id, artist_id, studio_id, workshop_id],
            )
            if not cursor.fetchone():
                cursor.execute(
                    """
                    INSERT INTO REGISTERS (MEMBER_ID, ARTIST_ID, STUDIO_ID, WORKSHOP_ID, REG_DATE)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    [member_id, artist_id, studio_id, workshop_id, reg_date],
                )
                messages.success(request, "Member registered successfully.")
            else:
                messages.warning(request, "Member is already registered for this workshop.")

    return redirect('workshop_detail',
                    artist_id=artist_id, studio_id=studio_id,
                    workshop_id=workshop_id)



def unregister_member(request, artist_id, studio_id, workshop_id, member_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM REGISTERS
                WHERE MEMBER_ID = %s AND ARTIST_ID = %s
                  AND STUDIO_ID = %s AND WORKSHOP_ID = %s
                """,
                [member_id, artist_id, studio_id, workshop_id],
            )
    return redirect('workshop_detail',
                    artist_id=artist_id, studio_id=studio_id,
                    workshop_id=workshop_id)




def log_consumption(request, artist_id, studio_id, workshop_id):
    if request.method == 'POST':
        material_id = request.POST.get('material_id')
        qty_used    = int(request.POST.get('qty_used', 0))

        with connection.cursor() as cursor:
            # 1. Check stock availability
            cursor.execute("SELECT QUANTITY_IN_STOCK, MAT_NAME FROM RAW_MATERIAL WHERE MATERIAL_ID = %s", [material_id])
            row = cursor.fetchone()
            
            if not row:
                messages.error(request, "Material not found.")
            elif row[0] < qty_used:
                messages.error(request, f"Insufficient stock for {row[1]}. Available: {row[0]}")
            else:
                # 2. Deduct from stock
                cursor.execute(
                    "UPDATE RAW_MATERIAL SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK - %s WHERE MATERIAL_ID = %s",
                    [qty_used, material_id]
                )

                # 3. Check existing consumption record
                cursor.execute(
                    """
                    SELECT QTY_USED FROM CONSUMES
                    WHERE ARTIST_ID = %s AND STUDIO_ID = %s
                      AND WORKSHOP_ID = %s AND MATERIAL_ID = %s
                    """,
                    [artist_id, studio_id, workshop_id, material_id],
                )
                existing = cursor.fetchone()

                if existing:
                    cursor.execute(
                        """
                        UPDATE CONSUMES
                        SET QTY_USED = QTY_USED + %s
                        WHERE ARTIST_ID = %s AND STUDIO_ID = %s
                          AND WORKSHOP_ID = %s AND MATERIAL_ID = %s
                        """,
                        [qty_used, artist_id, studio_id, workshop_id, material_id],
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO CONSUMES
                            (ARTIST_ID, STUDIO_ID, WORKSHOP_ID, MATERIAL_ID, QTY_USED)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        [artist_id, studio_id, workshop_id, material_id, qty_used],
                    )
                messages.success(request, f"Successfully logged {qty_used} of {row[1]}.")

    return redirect('workshop_detail',
                    artist_id=artist_id, studio_id=studio_id,
                    workshop_id=workshop_id)


def delete_consumption(request, artist_id, studio_id, workshop_id, material_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            # 1. Get the quantity that was used to return it to stock
            cursor.execute(
                """
                SELECT QTY_USED FROM CONSUMES
                WHERE ARTIST_ID = %s AND STUDIO_ID = %s
                  AND WORKSHOP_ID = %s AND MATERIAL_ID = %s
                """,
                [artist_id, studio_id, workshop_id, material_id]
            )
            row = cursor.fetchone()
            if row:
                qty = row[0]
                # 2. Return to stock
                cursor.execute(
                    "UPDATE RAW_MATERIAL SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK + %s WHERE MATERIAL_ID = %s",
                    [qty, material_id]
                )
                # 3. Delete record
                cursor.execute(
                    """
                    DELETE FROM CONSUMES
                    WHERE ARTIST_ID = %s AND STUDIO_ID = %s
                      AND WORKSHOP_ID = %s AND MATERIAL_ID = %s
                    """,
                    [artist_id, studio_id, workshop_id, material_id]
                )
                messages.success(request, "Material consumption entry removed and stock restored.")
    
    return redirect('workshop_detail',
                    artist_id=artist_id, studio_id=studio_id,
                    workshop_id=workshop_id)


def edit_consumption(request, artist_id, studio_id, workshop_id, material_id):
    if request.method == 'POST':
        new_qty = int(request.POST.get('qty_used', 0))
        
        with connection.cursor() as cursor:
            # 1. Get old qty
            cursor.execute(
                """
                SELECT QTY_USED FROM CONSUMES
                WHERE ARTIST_ID = %s AND STUDIO_ID = %s
                  AND WORKSHOP_ID = %s AND MATERIAL_ID = %s
                """,
                [artist_id, studio_id, workshop_id, material_id]
            )
            row = cursor.fetchone()
            if row:
                old_qty = row[0]
                diff = new_qty - old_qty # positive if we used more, negative if we used less
                
                # 2. Check stock if we are increasing consumption
                if diff > 0:
                    cursor.execute("SELECT QUANTITY_IN_STOCK FROM RAW_MATERIAL WHERE MATERIAL_ID = %s", [material_id])
                    stock = cursor.fetchone()[0]
                    if stock < diff:
                        messages.error(request, "Not enough stock to increase consumption.")
                        return redirect('workshop_detail', artist_id=artist_id, studio_id=studio_id, workshop_id=workshop_id)
                
                # 3. Update stock (decrement by diff)
                cursor.execute(
                    "UPDATE RAW_MATERIAL SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK - %s WHERE MATERIAL_ID = %s",
                    [diff, material_id]
                )
                
                # 4. Update consumption record
                cursor.execute(
                    """
                    UPDATE CONSUMES SET QTY_USED = %s
                    WHERE ARTIST_ID = %s AND STUDIO_ID = %s
                      AND WORKSHOP_ID = %s AND MATERIAL_ID = %s
                    """,
                    [new_qty, artist_id, studio_id, workshop_id, material_id]
                )
                messages.success(request, "Consumption quantity updated.")

    return redirect('workshop_detail',
                    artist_id=artist_id, studio_id=studio_id,
                    workshop_id=workshop_id)




def artist_list(request):
    """Shown as a section inside the workshops page."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT ARTIST_ID, FIRST_NAME, LAST_NAME, EMAIL, SPECIALTY
            FROM RESIDENT_ARTIST
            ORDER BY FIRST_NAME
            """
        )
        artists = cursor.fetchall()
    return render(request, 'artist_list.html', {'artists': artists})


def add_artist(request):
    error = None
    if request.method == 'POST':
        artist_id  = request.POST.get('artist_id')
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        email      = request.POST.get('email')
        specialty  = request.POST.get('specialty')

        if not all([artist_id, first_name, last_name, email]):
            error = "ID, first name, last name and email are required."
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO RESIDENT_ARTIST
                        (ARTIST_ID, FIRST_NAME, LAST_NAME, EMAIL, SPECIALTY)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    [artist_id, first_name, last_name, email, specialty],
                )
            return redirect('artist_list')

    return render(request, 'add_artist.html', {'error': error})


def edit_artist(request, artist_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT ARTIST_ID, FIRST_NAME, LAST_NAME, EMAIL, SPECIALTY
            FROM RESIDENT_ARTIST
            WHERE ARTIST_ID = %s
            """,
            [artist_id],
        )
        artist = cursor.fetchone()

    if not artist:
        return redirect('artist_list')

    error = None
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        email      = request.POST.get('email')
        specialty  = request.POST.get('specialty')

        if not all([first_name, last_name, email]):
            error = "First name, last name and email are required."
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE RESIDENT_ARTIST
                    SET FIRST_NAME = %s,
                        LAST_NAME  = %s,
                        EMAIL      = %s,
                        SPECIALTY  = %s
                    WHERE ARTIST_ID = %s
                    """,
                    [first_name, last_name, email, specialty, artist_id],
                )
            return redirect('artist_list')

    return render(request, 'edit_artist.html', {'artist': artist, 'error': error})


def delete_artist(request, artist_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM RESIDENT_ARTIST WHERE ARTIST_ID = %s",
                [artist_id],
            )
    return redirect('artist_list')


# ── Studio Management ──────────────────────────────────────

def studio_list(request):
    error = None
    edit_studio = None
    edit_id = request.GET.get('edit')

    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute("SELECT STUDIO_ID, STUDIO_NAME, LOCATION, CAPACITY, STUDIO_TYPE, EQUIPMENT FROM STUDIO WHERE STUDIO_ID = %s", [edit_id])
            edit_studio = cursor.fetchone()

    if request.method == 'POST':
        action = request.POST.get('action')
        
        studio_id = request.POST.get('studio_id')
        studio_name = request.POST.get('studio_name')
        location = request.POST.get('location') or None
        capacity = request.POST.get('capacity')
        studio_type = request.POST.get('studio_type') or None
        equipment = request.POST.get('equipment') or None
        
        # Numeric field handling
        if capacity == "" or capacity is None:
            capacity = None
        else:
            try:
                capacity = int(capacity)
            except ValueError:
                capacity = None

        if action == 'add':
            if not studio_id:
                error = "Studio ID is required."
            else:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            INSERT INTO STUDIO (STUDIO_ID, STUDIO_NAME, LOCATION, CAPACITY, STUDIO_TYPE, EQUIPMENT) 
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, [studio_id, studio_name, location, capacity, studio_type, equipment])
                    return redirect('studio_list')
                except Exception as e:
                    error = f"Error adding studio: {e}"
        elif action == 'edit':
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE STUDIO 
                        SET STUDIO_NAME = %s, LOCATION = %s, CAPACITY = %s, STUDIO_TYPE = %s, EQUIPMENT = %s 
                        WHERE STUDIO_ID = %s
                    """, [studio_name, location, capacity, studio_type, equipment, studio_id])
                return redirect('studio_list')
            except Exception as e:
                error = f"Error updating studio: {e}"
        elif action == 'delete':
            studio_id_to_delete = request.POST.get('studio_id')
            try:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM STUDIO WHERE STUDIO_ID = %s", [studio_id_to_delete])
                return redirect('studio_list')
            except Exception as e:
                error = f"Cannot delete studio. It might be linked to workshops. Error: {e}"

    with connection.cursor() as cursor:
        cursor.execute("SELECT STUDIO_ID, STUDIO_NAME, LOCATION, CAPACITY, STUDIO_TYPE, EQUIPMENT FROM STUDIO ORDER BY STUDIO_NAME")
        studios = cursor.fetchall()

    return render(request, 'studio_list.html', {
        'studios': studios,
        'edit_studio': edit_studio,
        'error': error
    })