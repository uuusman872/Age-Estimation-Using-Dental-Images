"""fyp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pathlib import Path
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from dashboard import views
urlpatterns = [

    path('doctor_dashboard', views.doctor_dashboard, name="doctor_dashboard"),
    path('doctor_form', views.doctor_form, name="doctor_form"),
    path('doctor_table', views.doctor_table, name="doctor_table"),
    path('age_estimation', views.age_estimation, name="age_estimation"),
    path('update/<int:patient_id>', views.update),
    path('delete/<int:patient_id>', views.delete),
    path('forensic_dashboard', views.forensic_dashboard, name="forensic_dashboard"),
    path('patient_dashboard', views.patient_dashboard, name="patient_dashboard"),
    path('generate_report',views.generate_report, name="generate_report"),
    path('forensic_request',views.forensic_request, name="forensic_request"),
    path('forensic_reject/<int:p_id>', views.forensic_reject),
    path('forensic_accept/<int:p_id>', views.forensic_accept),
    path('forensic_delete/<int:p_id>', views.forensic_delete),
    path('forensic_accepted_request',views.forensic_accepted_request, name="forensic_accepted_request"),
    path('gernerate_age_report',views.generate_age_report, name="gernerate_age_report"),
    path('age_estimation_form/<int:image_id>',views.age_estimation_form, name="age_estimation_form"),
    path('noise_remove/<int:image_id>',views.noise_remove, name="noise_remove"),
    path('forensic_appointments', views.forensic_appointments, name="forensic_appointments"),
    path('doctors_list', views.doctors_list, name="doctors_list"),
    path('report/<int:image_id>', login_required(views.GeneratePDF.as_view()), name="report"),
    path("FormPageForForensicAgent/<int:userid>", views.FormPageForForensicAgent, name="FormPageForForensicAgent"),
    path("doctor_detai/<int:doc_id>", views.doctor_detai, name="doctor_detai"),
    path("DoctorAppointmentFormPage:<int:doc_id>", views.DoctorAppointmentFormPage, name="DoctorAppointmentFormPage"),
    path("doctor_detai/InboxMessages/<int:doc_id>" , views.InboxMessages, name="InboxMessages"),
    path('doctor_reject/<int:p_id>', views.doctor_reject),
    path('doctor_accept/<int:p_id>', views.doctor_accepet),
    path("FormPageForDoctor/<int:userid>", views.FormPageForDoctor, name="FormPageForDoctor"),
    path("doctor_suggestions", views.doctor_suggestions, name="doctor_suggestions"),
    path("paitentMessage", views.PaitentQuestionForm, name='paitentMessage'),
    path("handleMessaageForm/<int:qid>", views.handleMessaageForm, name="handleMessaageForm"),\
    path("get_location/<int:pk>", views.get_location.as_view(), name="get_location"),
    path("models", views.models, name="models"),
    path('svm/<int:image_id>',views.svm, name="svm"),
    path('knn/<int:image_id>',views.knn, name="knn"),
    path('resnet/<int:image_id>',views.resnet, name="resnet"),          

  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
