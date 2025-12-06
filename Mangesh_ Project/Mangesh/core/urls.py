from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('signup/doctor/', views.doctor_signup, name='doctor_signup'),
    path('signup/patient/', views.patient_signup, name='patient_signup'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/availability/add/', views.add_availability, name='add_availability'),

    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
]
