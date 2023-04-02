from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:pk>/save_availability/', views.save_availability, name='save_availability'),
    path('doctors/<int:pk>/update_availability/', views.update_availability, name='update_availability'),
    path('doctors/<int:pk>/list_availability/', views.list_availability, name='list_availability'),
]
