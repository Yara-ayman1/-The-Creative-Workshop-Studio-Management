from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup_member, name='signup_member'),
    path('login/', views.login_member, name='login_member'),
    path('profile/', views.profile_member, name='profile_member'),
   


]
