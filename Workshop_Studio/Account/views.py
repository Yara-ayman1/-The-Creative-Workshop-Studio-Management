from datetime import datetime, timedelta
from django.db import connection
from django.shortcuts import render,redirect

#signup
def signup_member(request):
 if request.method == 'POST':
    f_name = request.POST.get('first_name')
    l_name = request.POST.get('last_name')
    mail = request.POST.get('email')
    
    pho = request.POST.get('phone')
    m_type = request.POST.get('member_type')
    start_date = datetime.now()
    end_date = start_date + timedelta(days=365)
   
    with connection.cursor() as cursor:
            
            query = """
                INSERT INTO MEMBER (first_name, last_name, email, phone, 
                                    membership_start, membership_end, membership_type) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, [f_name, l_name, mail, pho, start_date, end_date, m_type])
            
    return redirect('login_member')
    

 return render(request, 'signup.html')

#login
def login_member(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
       
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Member WHERE CONCAT(first_name, ' ', last_name) = %s AND email = %s", [user_name, email])
            member = cursor.fetchone()
            if member:
                request.session['member_id']=member[0]
                return redirect('profile_member')
            else:
                return render(request, 'login.html', {'error': 'Invalid username or Email'})
    return render(request, 'login.html')

#profile
def profile_member(request):
    m_id=request.session.get('member_id')
    if not m_id:
         return redirect('login_member')
    with connection.cursor() as cursor:
         cursor.execute("""
            SELECT FIRST_NAME, LAST_NAME, EMAIL, PHONE, MEMBERSHIP_TYPE, 
            membership_start, membership_end, MEMBER_ID 
            FROM MEMBER 
            WHERE MEMBER_ID = %s  
            """,[m_id])
         member_data =cursor.fetchone()
    context ={
        'first_name':member_data[0],
        'last_name':member_data[1],
        'email':member_data[2], 
        'phone': member_data[3],
        'membership': member_data[4],
        'start_date': member_data[5],
        'end_date': member_data[6],  
        'member_id': member_data[7], 
        } 
       

       
    return render(request, 'profile.html',context)    
