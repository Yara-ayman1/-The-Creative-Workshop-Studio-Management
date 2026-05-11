from django.urls import path
from . import views
urlpatterns = [
    path('', views.manage_members, name='MembersList'),
    path('add_member/', views.add_member, name='AddMemberForm'),
    path('edit_member/<int:member_id>/', views.edit_member, name='edit_member'),
    path('delete_member/<int:member_id>/', views.delete_member, name='delete_member'),
   
    


]
