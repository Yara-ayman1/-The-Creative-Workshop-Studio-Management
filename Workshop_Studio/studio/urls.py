from django.urls import path
from . import views

urlpatterns = [

    path('', views.studio_list, name='studio_list'),
    path('add/', views.add_studio,name='add_studio'),
    path('deactivate/<int:studio_id>/', views.deactivate_studio, name='deactivate_studio'),

]