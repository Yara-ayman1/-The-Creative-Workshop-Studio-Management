from datetime import datetime, timedelta
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages

def manage_members(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM MEMBER")
        members = cursor.fetchall()
    return render(request, 'MembersList.html', {'members': members})

def add_member(request):
 if request.method == 'POST':
    f_name = request.POST.get('first_name')
    l_name = request.POST.get('last_name')
    mail = request.POST.get('email')
    
    pho = request.POST.get('phone')
    m_type = request.POST.get('member_type')
    start_date = request.POST.get('membership_start')
    end_date = request.POST.get('membership_end')
    
   
    with connection.cursor() as cursor:
            
            query = """
                INSERT INTO MEMBER (first_name, last_name, email, phone, 
                                    membership_start, membership_end, membership_type) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, [f_name, l_name, mail, pho, start_date, end_date, m_type])
            
    return redirect('MembersList')
    

 return render(request, 'AddMemberForm.html')
def edit_member(request, member_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM MEMBER WHERE MEMBER_ID = %s", [member_id])
        member = cursor.fetchone()
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        mail = request.POST.get('email')
        pho = request.POST.get('phone')
        m_type = request.POST.get('member_type')
        start_date = request.POST.get('membership_start')
        end_date = request.POST.get('membership_end')
        
        with connection.cursor() as cursor:
            query = """
                UPDATE MEMBER 
                SET first_name = %s, last_name = %s, email = %s, phone = %s, 
                    membership_start = %s, membership_end = %s, membership_type = %s 
                WHERE MEMBER_ID = %s
            """
            cursor.execute(query, [f_name, l_name, mail, pho, start_date, end_date, m_type, member_id])
            
        return redirect('MembersList')
    
    return render(request, 'edit_member.html', {'member': member})


def delete_member(request, member_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM RENTS WHERE MEMBER_ID = %s", [member_id])
        rents_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM REGISTERS WHERE MEMBER_ID = %s", [member_id])
        registers_count = cursor.fetchone()[0]

        if rents_count or registers_count:
            reasons = []
            if rents_count:
                reasons.append(f"{rents_count} rent record{'s' if rents_count != 1 else ''}")
            if registers_count:
                reasons.append(f"{registers_count} registration record{'s' if registers_count != 1 else ''}")
            messages.error(
                request,
                "Cannot delete member. This member is still referenced by " +
                " and ".join(reasons) + ". Remove those records first."
            )
        else:
            cursor.execute("DELETE FROM MEMBER WHERE MEMBER_ID = %s", [member_id])
            messages.success(request, "Member deleted successfully.")

    return redirect('MembersList')



 
