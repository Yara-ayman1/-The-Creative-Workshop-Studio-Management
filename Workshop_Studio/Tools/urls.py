from django.urls import path
from . import views

urlpatterns = [
    path('', views.tool_dashboard, name='tool_dashboard'),
    path('rent_tool/', views.rent_tool, name='rent_tool'),
    path('return_tool/', views.return_tool, name='return_tool'),
    path('add_tool/', views.add_tool, name='add_tool'),
    path('delete_tool/', views.delete_tool, name='delete_tool'),
]