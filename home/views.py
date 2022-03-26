
from django.shortcuts import render,HttpResponse
from accounts.models import CustomUser,SomeLocationModel
from .models import models
from .forms import Contact

# Create your views here.

def index(request):
    
    all_objects = CustomUser.objects.filter(is_doctor=True)[:3]
    all_location= SomeLocationModel.exportlocation()
    all_agents= CustomUser.objects.filter(is_forensic = True)[:3]
    all_doctors = CustomUser.objects.filter(is_doctor=True).count()
    all_forensic= CustomUser.objects.filter(is_forensic = True).count()
    all_patient= CustomUser.objects.filter(is_patient = True).count()
    all_users= CustomUser.objects.all().count() - 1
    form = Contact(request.POST)
    if form.is_valid():
        form.save()
        
    # context = {
    #     "doctor_list" : all_objects,
    #     "doctor_location" : all_location 
    # }
    mylist = zip(all_objects , all_location)
    return render(request, "index.html",{'list': mylist , "form" : form , "agents": all_agents , "all_doctors" : all_doctors, "all_forensic" : all_forensic , "all_patient" : all_patient, "all_users" : all_users})

def services(request):
    return render(request,"services.html")

def services1(request):
    return render(request,"services1.html")

def suggest(request):
    return render(request,"suggestion.html")

def doctor_profile_page(request):
    all_objects = CustomUser.exportDoctors()
    all_location= SomeLocationModel.exportlocation()
    
    # context = {
    #     "doctor_list" : all_objects,
    #     "doctor_location" : all_location 
    # }
    mylist = zip(all_objects , all_location)

    return render(request,"doctor_profile_page.html" , {'list': mylist})