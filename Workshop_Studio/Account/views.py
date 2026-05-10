from datetime import datetime, timedelta
from django.db import connection
from django.shortcuts import render,redirect

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
def login_member(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
       
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Member WHERE CONCAT(first_name, ' ', last_name) = %s AND email = %s", [user_name, email])
            member = cursor.fetchone()
            if member:
                return redirect('profile_member')
            else:
                return render(request, 'login.html', {'error': 'Invalid username or Email'})
    return render(request, 'login.html')
def profile_member(request):
    # كود مؤقت عشان الصفحة تفتح معاكي
    return render(request, 'profile.html')

# Create your views here.
