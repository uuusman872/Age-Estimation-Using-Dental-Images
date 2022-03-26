from django.contrib import admin
from django.urls import path,include
from accounts import views
from.views import VerificationView
from django.contrib.auth import views as auth_views

urlpatterns = [


    path('registration', views.registration, name="registration"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('doctor_register', views.doctor_register.as_view(), name="doctor_register"),
    path('patient_register', views.patient_register.as_view(), name="patient_register"),
    path('forensic_register', views.forensic_register.as_view(), name="forensic_register"),
    path('profile', views.profile, name="profile"),
    path('activate/<uidb64>/<token>',VerificationView.as_view(), name="activate"),
    path('patient_profile', views.patient_profile, name="patient_profile"),
    path('forensic_profile', views.forensic_profile, name="forensic_profile"),
    path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]