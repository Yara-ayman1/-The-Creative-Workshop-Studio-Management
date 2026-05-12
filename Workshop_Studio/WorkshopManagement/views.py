from django.shortcuts import render, redirect
from django.db import connection




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
            SELECT rm.MAT_NAME, rm.UNIT, c.QTY_USED
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
                # Redirect back; capacity full (could add a flash message)
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
            # Check existing record
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

            # Deduct from stock
            cursor.execute(
                """
                UPDATE RAW_MATERIAL
                SET QUANTITY_IN_STOCK = QUANTITY_IN_STOCK - %s
                WHERE MATERIAL_ID = %s AND QUANTITY_IN_STOCK >= %s
                """,
                [qty_used, material_id, qty_used],
            )

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