from django.forms.widgets import PasswordInput, TextInput
from .models import Doctor, Patient , CustomUser,Forensic
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.core.mail import EmailMessage
from django.shortcuts import render,redirect , HttpResponse
from django.views.generic import View
from django import forms
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from .utilts import account_activation_token
from .models import SomeLocationModel
from mapbox_location_field.models import LocationField
class ProfileForm(ModelForm):
    profile_image = forms.ImageField( widget=forms.FileInput)
    class Meta:
        model = CustomUser
        fields = [
         'profile_image',
         'first_name',
         'last_name',
         'phone_number',
        ]
    
class LocationForm(forms.ModelForm):
    
    class Meta:  
        model = SomeLocationModel 
        fields = [
            'location'
        ]

class DoctorForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number= forms.IntegerField( required = True)
    
    Cnic = forms.IntegerField( required = True)
    Certificate= forms.FileField( required= True)
    Qualification= forms.CharField(required= True)
    
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["first_name", "last_name","username" , "email" , "password1", "password2", "phone_number", "Cnic", "Certificate" ,"Qualification"]        
    
    # def cleaasdasdn_username(self):
    #     user = self.cleaned_data['username']
    #     try:
    #         match = CustomUser.objects.get(username=user)
    #     except:
    #         return self.cleaned_data['username']
    #     raise forms.ValidationError("dasssssssssssssssssssssssssssssssssssssssssssssssss")


    @transaction.atomic
    def save(self):
        user= super().save(commit=False)
        user.is_doctor = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        
        user.is_active = False
        user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.Cnic = self.cleaned_data.get('Cnic')
        doctor.Certificate = self.cleaned_data.get('Certificate')
        doctor.Qualification = self.cleaned_data.get('Qualification')
        doctor.save()
        return user






class PatientForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number= forms.IntegerField( required = True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["first_name", "last_name","username" , "email" , "password1", "password2", "phone_number"]       

    @transaction.atomic
    def save(self):
        user= super().save(commit=False)
        user.is_patient = True
        user.is_approve = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        user.save()
        patient = Patient.objects.create(user=user)
        # patient.medical_history = self.cleaned_data.get('medical_history')
        # patient.age = self.cleaned_data.get('age')
        patient.save()
        return user


class ForensicForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number= forms.IntegerField( required = True)
    email = forms.EmailField(required=True)
    Certificate= forms.FileField(required= True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["first_name", "last_name","username" , "email" , "password1", "password2", "phone_number", "Certificate" ] 
   

    @transaction.atomic
    def save(self):
        user= super().save(commit=False)
        user.is_forensic = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        user.is_active = False
        user.save()
        forensic = Forensic.objects.create(user=user)
        forensic.Certificate = self.cleaned_data.get('Certificate2')
        forensic.save()
        return user


from .models import QuestionModel

class QuestionModelForm(forms.ModelForm):
    class Meta():
        model = QuestionModel
        fields = ["Question"]

class AnswerModelForm(forms.ModelForm):
    class Meta():
        model = QuestionModel
        fields = ["Answers"]

# class AnswersQuestionModelForm(forms.ModelForm):
#     class Meta():
#         model = AnswersQuestionModel
#         fields = ["Answers"]
