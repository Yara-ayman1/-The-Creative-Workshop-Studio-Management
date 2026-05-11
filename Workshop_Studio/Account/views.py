from datetime import datetime, timedelta
from django.db import connection
from django.shortcuts import render,redirect

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
        cursor.execute("DELETE FROM MEMBER WHERE MEMBER_ID = %s", [member_id])
    return redirect('MembersList')



 
