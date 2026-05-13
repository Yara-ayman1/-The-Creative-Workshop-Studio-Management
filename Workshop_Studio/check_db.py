from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("EXEC sp_pkeys 'RENTS'")
    print("RENTS PK:", cursor.fetchall())
    cursor.execute("SELECT WORKSHOP_DATE, TITLE, CRAFT_TYPE FROM WORKSHOP")
    print("Workshops:", cursor.fetchall())
