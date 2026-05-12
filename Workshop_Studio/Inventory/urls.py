from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_dashboard, name='inventory_dashboard'),
    path('add-material/', views.add_material, name='add_material'),
    path('record-consumption/', views.record_consumption, name='record_consumption'),
    path('increase_stock/', views.increase_stock, name='increase_stock'),
    path('delete_material/', views.delete_material, name='delete_material'),
]