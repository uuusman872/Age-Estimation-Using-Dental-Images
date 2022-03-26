from django.shortcuts import render,redirect , HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic import CreateView
from .models import Doctor, Patient , CustomUser,SomeLocationModel,Forensic
from .forms import DoctorForm ,PatientForm ,ProfileForm, LocationForm,ForensicForm
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from .forms import LocationForm
from django.core.mail import EmailMessage
from django.views.generic import View
from django import forms
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from .utilts import account_activation_token
from .decorators import *
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_excluded('/')
def login(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
    
            if user is not None:
                if user.is_approve == False:
                    messages.warning(request,"Wait for Account Approval!")
                else:
                    auth.login(request,user)
                    if user.is_doctor == True:
                        return redirect('doctor_dashboard')
                    if user.is_forensic == True:
                        return redirect('forensic_dashboard')
                    if user.is_patient == True:
                        return redirect('patient_dashboard')
                        

            else:
                messages.warning(request,"Invalid username or password")

        else:
                messages.warning(request,"Invalid username or password")
    return render(request, 'login.html',
    context={'form':AuthenticationForm()})
    
    
@login_excluded('/')
def registration(request):
    return render(request,"registration.html")

# where name is the name of the method to be decorated.
# or in case of few decorators:
# decorators = [never_cache, login_required]
# @method_decorator(decorators, name='dispatch')
# class YourClassBasedView(TemplateView):

@method_decorator(login_excluded('/'), name='dispatch')
class doctor_register(CreateView):
    model = CustomUser
    form_class = DoctorForm
    mymap = LocationForm
    extra_context={'mymap': mymap}
    template_name = "doctor_register.html"

    def form_valid(self, form):
        try:
            user = form.save()
            loc = self.request.POST["location"]
            mm = SomeLocationModel.objects.create(user=user, location=loc)
            print("The Location got is ", self.request.POST["location"])
            if mm.is_valid():
                mm.save()
        
        except Exception as ex:
            pass
    
        
        # mymap = LocationForm()
        # try:
        #     mymap = LocationForm(self.request.POST or None)
        #     mymap.location= form.cleaned_data.get('location')
        #     mymap= SomeLocationModel.objects.create(user=user)
        #     print(mymap.cleaned_data.get('location'))
        #     mymap.save()
        # except Exception as ex:
        #    pass
        # if self.request.method == 'POST':
        #     mmmap= SomeLocationModel.objects.create(user=user)
        #     mmmap.location = self.form.cleaned_data.get('location')
        #     mmmap.save()




        uidb64=urlsafe_base64_encode(force_bytes(user.pk))

        domain= get_current_site(self.request).domain

        link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': account_activation_token.make_token(user)})
        
        activate_url='http://'+domain+link         

        # email_body='Hi ' + user.username + " Please use this link to verify account\n "+ activate_url
        
        # email_subject="Activate your account"

        # email = EmailMessage(
        #     email_subject,
        #     email_body,
        #     'noreply@example.com',
        #     [user.email],
        # )


        # email.send(fail_silently=False)
        messages.success(self.request,"Account Successfully Created! Please Verify Email")
        return redirect('login')

class VerificationView(View):
    def get(self,request,uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                messages.warning(request, 'Email already Verified!' )
                return redirect('login'+'?message='+'Email already Verified!')

            if user.is_active:
                return redirect('login')

            user.is_active = True
            user.save()

            messages.success(request, 'Email Verified!\n Please wait for admin approval.' )
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')

        
@method_decorator(login_excluded('/'), name='dispatch')
class patient_register(CreateView):
    model = CustomUser
    form_class = PatientForm
    template_name = "patient_register.html"

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request,"Account Successfully Created!")
        return redirect('patient_dashboard')


@method_decorator(login_excluded('/'), name='dispatch')
class forensic_register(CreateView):
    model = CustomUser
    form_class = ForensicForm
    template_name = "forensic_register.html"

    def form_valid(self, form):
        user = form.save()
        uidb64=urlsafe_base64_encode(force_bytes(user.pk))

        domain= get_current_site(self.request).domain

        link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': account_activation_token.make_token(user)})
        
        activate_url='http://'+domain+link         

        email_body='Hi ' + user.username + " Please use this link to verify account\n "+ activate_url
        
        email_subject="Activate your account"

        email = EmailMessage(
            email_subject,
            email_body,
            'noreply@example.com',
            [user.email],
        )


        email.send(fail_silently=False)
        messages.warning(self.request,"Account Successfully Created! Please Verify Email")
        return redirect('login')


def logout(request):
    auth.logout(request)
    return redirect("/")

@login_required
def profile(request):
    user= request.user
    form = ProfileForm(instance=user)
    if request.method == 'POST':
        form= ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile Updated!")
    context = { 'form' : form}
    return render(request,"doctor/profile.html" ,context)

@login_required
def patient_profile(request):
    user= request.user
    form = ProfileForm(instance=user)
    if request.method == 'POST':
        form= ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile Updated!")
    context = { 'form' : form}
    return render(request,"patient/patient_profile.html" ,context)

@login_required
def forensic_profile(request):
    user= request.user
    form = ProfileForm(instance=user)
    if request.method == 'POST':
        form= ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile Updated!")
            
    context = { 'form' : form}
    
    return render(request,"forensic/forensic_profile.html" ,context)