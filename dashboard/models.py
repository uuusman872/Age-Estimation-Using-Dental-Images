from django.db import models
from datetime import datetime
from django.utils import timezone
from accounts.models import CustomUser
import os
# Create your models here.
#DataFlair Models
class PatientRecord(models.Model):
    user= models.ForeignKey(CustomUser,  on_delete=models.CASCADE, null= True, blank= True)
    name = models.CharField(max_length = 50, blank=False)
    image = models.ImageField()
    desc = models.TextField(max_length = 100, default='No Description')
    Phone = models.PositiveIntegerField()
    Age = models.PositiveIntegerField()
    Date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name



class ForensicImageRecord(models.Model):
    image = models.ImageField(upload_to="ForensicImages")


class ForensicAppointmentRequests(models.Model):
    user= models.ForeignKey(CustomUser,  on_delete=models.CASCADE, null= True, blank= True)
    image = models.ImageField(upload_to="ForensicAppointments")
    desc = models.TextField(max_length = 100, default='' )
    status = models.BooleanField(default=False)
    forensic_agent_id = models.CharField(max_length=200, default="", null=True, blank=True)
    date= models.DateTimeField(blank=True,null=True, default=datetime.now())

# class AppointmentRequestDoctor(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null= True, blank= True)
#     doctor_id = models.IntegerField()
#     desc = models.TextField()
#     status = models.BooleanField()
#     report = models.FileField(upload_to="document")

class AppointmentDoctorModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null= True, blank= True)
    doctor_id = models.IntegerField()
    desc = models.TextField()
    status = models.BooleanField(default=False)
    report = models.FileField(upload_to="document")
    date= models.DateTimeField(blank=True,null=True, default= datetime.now())

class PaitentForensicAppointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null= True, blank= True)
    username = models.CharField(max_length=100, default='', null=True, blank=True)
    desc = models.TextField()
    flie = models.FileField(upload_to="document")
    date= models.DateTimeField(blank=True,null=True, default= datetime.now())
    


# class PaitentDoctorReports(models.Model):
#     User = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null= True, blank= True)
#     Description = models.TextField()
#     Report = models.FileField(upload_to="PaitentDoctorReport")


class DatabaseForPaitentDoctor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null= True, blank= True)
    DoctorName = models.CharField(default='', null=True, blank=True, max_length=100)
    suggestions = models.TextField()
    flie = models.FileField(upload_to="document")
    date= models.DateTimeField(blank=True,null=True, default= datetime.now())