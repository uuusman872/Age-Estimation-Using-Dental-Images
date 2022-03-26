from django.db import models
from django.contrib.auth.models import AbstractUser  
from mapbox_location_field.models import LocationField,AddressAutoHiddenField

class CustomUser(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient =models.BooleanField(default=False)
    is_forensic =models.BooleanField(default=False)
    is_approve =models.BooleanField(default=False)
    first_name= models.CharField( max_length=50)
    last_name= models.CharField( max_length=50)
    phone_number= models.CharField( max_length=50 , unique=True)
    email = models.EmailField(max_length= 50, unique=True )
    profile_image = models.ImageField(default="ASD.jpg" , blank= True, null= True, )
    

    def exportDoctors():
        all_objects = CustomUser.objects.filter(is_doctor=True)
        return all_objects
        

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    Cnic = models.CharField( max_length=50 , unique=True)
    Certificate = models.FileField(upload_to="document", blank=True , null=True)
    Qualification = models.CharField( max_length=50)

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    medical_history= models.CharField( max_length=50)
    

class Forensic(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    Certificate= models.FileField(upload_to="document", blank=True , null=True)
    

class SomeLocationModel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    location = LocationField(map_attrs={"rotate": True, "marker_color": "blue", })
    address = AddressAutoHiddenField()

    def exportlocation():
        all_location = SomeLocationModel.objects.all()
        return all_location

class QuestionModel(models.Model):
    User = models.ForeignKey(CustomUser(), on_delete=models.CASCADE)
    doc_id = models.IntegerField(max_length=100, default=None)
    Question = models.CharField(max_length=100)
    Answers = models.CharField(default='', null=True, blank=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    Author = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

# class AnswersQuestionModel(models.Model):
#     AnsQuestion = models.ForeignKey(QuestionModel ,on_delete=models.CASCADE)
#     Answers = models.TextField()
#     Answered_at = models.DateTimeField(auto_now_add=True)
#     status = models.BooleanField(default=False)