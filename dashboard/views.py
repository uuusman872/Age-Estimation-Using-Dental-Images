from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from tensorflow.keras.preprocessing import image
from tensorflow.python.keras.optimizers import get
from .models import PatientRecord,DatabaseForPaitentDoctor
from .forms import PatientCreate, ForensicImageUploadingForm
from accounts.models import CustomUser,SomeLocationModel,Doctor
from django.contrib import messages
from accounts.decorators import *
from .models import AppointmentDoctorModel
from .forms import DatabaseForPaitentDoctorForm
from accounts.models import CustomUser
from .forms import ForensicAppointmentRequestForm
from .models import ForensicAppointmentRequests
from .forms import ForensicAppointmentRequestForm
from .models import ForensicAppointmentRequests
from .forms import PaitentForensicAppointmentForm
from accounts.models import CustomUser
from accounts.forms import AnswerModelForm, LocationForm
from accounts.forms import QuestionModelForm
from accounts.models import QuestionModel
from .forms import DoctorAppointmentRequestForm
from .models import PaitentForensicAppointment
from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf #created in step 4
from AgeEstimationModel.AgeEstimator import estimaeAge,removeNoise,SvmMode,KnnModel
from django.utils.decorators import method_decorator


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ Doctor
@login_required
@patient_forensic_not_allowed_on_doctor('/')
def doctor_dashboard(request):
    
    Requests = AppointmentDoctorModel.objects.filter(status= False).filter(doctor_id=request.user.id).count()
    Appointments = AppointmentDoctorModel.objects.filter(status=True).filter(doctor_id=request.user.id).count()
    Questions = QuestionModel.objects.filter(status=False).filter(doc_id=request.user.id).count()
    

   
    context = {
        'Requests' : Requests,
        "Appointments":Appointments,
        "Questions" : Questions
    }
    return render(request,"doctor/doctor_dashboard.html", context)


@login_required
@patient_forensic_not_allowed_on_doctor('/')
def doctor_form(request):
    patients=PatientRecord.objects.all()
    DoctorRequest = AppointmentDoctorModel.objects.filter(status=True).filter(doctor_id=request.user.id)
    context = {
        'patients' : patients,
        "DoctorRequest":DoctorRequest
    }
    return render(request,"doctor/doctor_form.html", context)


@login_required
@patient_forensic_not_allowed_on_doctor('/')
def update(request, patient_id):
    patient_id = int(patient_id)
    try:
        get_patient = PatientRecord.objects.get(id = patient_id)
    except PatientRecord.DoesNotExist:
        return redirect('doctor_table')
    form = PatientCreate( instance = get_patient)
    if request.method == 'POST':
        form = PatientCreate(request.POST or None,request.FILES, instance = get_patient)
        if form.is_valid():
            form.save()
            return redirect('doctor_table')
    return render(request, "doctor/doctor_form.html", {'form':form})

#patient request

@login_required
@patient_forensic_not_allowed_on_doctor('/')
def doctor_table(request):
    patients=PatientRecord.objects.all()
    DoctorRequest = AppointmentDoctorModel.objects.filter(status= False).filter(doctor_id=request.user.id)


    context = {
        'patients' : patients,
        "DoctorRequest":DoctorRequest
    }
    
    return render(request, "doctor/doctor_table.html", context=context)

@login_required
@patient_forensic_not_allowed_on_doctor('/')
def doctor_accepet(request,p_id):
    p_id= int(p_id)
    try:
        get_p= AppointmentDoctorModel.objects.get(pk = p_id)
        get_p.status = True
        get_p.save()
        messages.success(request, "Patient Appointment Accepted!")
    except AppointmentDoctorModel.DoesNotExist:
        return redirect("doctor_table")

    return redirect("doctor_table")


@login_required
@patient_forensic_not_allowed_on_doctor('/')
def doctor_reject(request,p_id):
    p_id= int(p_id)
    try:
        get_p= AppointmentDoctorModel.objects.get(pk = p_id)
        messages.warning(request, "Patient Appointment Rejected!")
    except AppointmentDoctorModel.DoesNotExist:
        return redirect("doctor_table")
    get_p.delete()
    return redirect("doctor_table")


@login_required
@patient_forensic_not_allowed_on_doctor('/')
def delete(request, patient_id):
    patient_id= int(patient_id)
    try:
        get_p= AppointmentDoctorModel.objects.get(pk = patient_id)
        messages.warning(request, "Patient Appointment Deleted!")
    except AppointmentDoctorModel.DoesNotExist:
        return redirect("doctor_form")
    get_p.delete()
    return redirect("doctor_form")


@login_required
@patient_forensic_not_allowed_on_doctor('/')
def FormPageForDoctor(request, userid):
    form = DatabaseForPaitentDoctorForm(request.POST, request.FILES)
    user = CustomUser.objects.filter(id=userid)[0] # Change to get
    print("[+] User " , userid)
    print("[+] User ", user)
    print(f"[+] user name is {user.first_name} {user.last_name}")
    print("[+] User ", type(request.user))
    print("[+] DoctorName ", request.user.first_name + " " + request.user.last_name)
    
    context = {"form":form}
    if form.is_valid():
        print("[+] Form is valid")
        savedForm = form.save(commit=False)
        savedForm.user = user
        savedForm.DoctorName = request.user.first_name + " " + request.user.last_name
        form.save()
        messages.success(request, "Send Suggestion Successfully!")
        
    return render(request, "doctor/FormPageForDoctor.html", context=context)


@login_required
@patient_forensic_not_allowed_on_doctor('/')
def PaitentQuestionForm(request):
    AnswerForm = AnswerModelForm(request.POST or None)
    Questions = QuestionModel.objects.filter(status=False).filter(doc_id=request.user.id)
    context = {
        "form":AnswerForm,
        "Questions":Questions
    }
    return render(request, "doctor\paitentMessage.html", context=context)


#Foresnic ......................................................................

@login_required
@doctor_patient_not_allowed_on_forensic('/')
def forensic_dashboard(request):
    AppointmentRequest = ForensicAppointmentRequests.objects.filter(status=False).count()
    AcceptedRequest = ForensicAppointmentRequests.objects.filter(status=True).count()
    return render(request,"forensic/forensic_dashboard.html", context={"AppointmentRequest":AppointmentRequest, "AcceptedRequest":AcceptedRequest})


@login_required
@doctor_patient_not_allowed_on_forensic('/')
def forensic_request(request):
    AppointmentRequest = ForensicAppointmentRequests.objects.filter(status=False)
    return render(request, "forensic/forensic_request.html",  context={"AppointmentRequest":AppointmentRequest})


@login_required
@doctor_patient_not_allowed_on_forensic('/')
def forensic_accepted_request(request):
    AcceptedRequest = ForensicAppointmentRequests.objects.filter(status=True).filter(forensic_agent_id=request.user.id)
    return render(request,"forensic/forensic_accept.html", context={ "AcceptedRequest":AcceptedRequest})


@login_required
@doctor_patient_not_allowed_on_forensic('/')
def FormPageForForensicAgent(request, userid):
    form = PaitentForensicAppointmentForm(request.POST, request.FILES)
    user = CustomUser.objects.filter(id=userid)[0] # Change to get
    print("[+] User " , userid)
    print("[+] User ", user)
    print("[+] User ", type(request.user))
    context = {"form":form}
    if form.is_valid():
        print("[+] Form is valid")
        savedForm = form.save(commit=False)
        savedForm.user = user
        savedForm.username = request.user.first_name + " " + request.user.last_name
        form.save()
        messages.success(request, "Successfully Sent!")
        
    return render(request, "forensic/ForensicPaitentForm.html", context=context)


@login_required
@doctor_patient_not_allowed_on_forensic('/')
def generate_age_report(request):
    return render(request, "forensic/gernerate_age_report.html" )


@login_required
@doctor_patient_not_allowed_on_forensic('/')
def forensic_accept(request,p_id):
    p_id= int(p_id)
    try:
        get_p= ForensicAppointmentRequests.objects.get(pk = p_id)
        get_p.status = True
        get_p.forensic_agent_id = request.user.id
        get_p.save()
        messages.success(request, "Successfully Accepted!")
    except ForensicAppointmentRequests.DoesNotExist:
        return redirect("forensic_request")
    return redirect("forensic_request")



@login_required
@doctor_patient_not_allowed_on_forensic('/')
def forensic_reject(request,p_id):
    p_id= int(p_id)
    try:
        get_p= ForensicAppointmentRequests.objects.get(pk = p_id)
        messages.success(request, "Successfully Rejected!")
    except ForensicAppointmentRequests.DoesNotExist:
        return redirect("forensic_request")
    get_p.delete()
    return redirect("forensic_request")


@login_required
@doctor_patient_not_allowed_on_forensic('/')
def forensic_delete(request,p_id):
    p_id= int(p_id)
    try:
        get_p= ForensicAppointmentRequests.objects.get(pk = p_id)
        messages.success(request, "Successfully Deleted!")
    except ForensicAppointmentRequests.DoesNotExist:
        return redirect("forensic_accepted_request")
    get_p.delete()
    return redirect("forensic_accepted_request")


from django.http import JsonResponse
from django.utils.safestring import mark_safe


#AGE ESTIMATION OLD FUNCTION 
@login_required
@doctor_patient_not_allowed_on_forensic('/')
def age_estimation_form(request, image_id):
    image_id= int(image_id)
    get_image= ForensicAppointmentRequests.objects.get(pk= image_id)
    imageforage= str(get_image.image)
    print("sadddddddddd" , imageforage)
    Age = estimaeAge( "media/" +imageforage)
    request.session["Age1"] = Age  
    messages.success(request,mark_safe( "Age : "+  Age))
    return redirect("age_estimation")

  
@login_required
@doctor_patient_not_allowed_on_forensic('/')
def noise_remove(request, image_id):
    image_id= int(image_id)
    get_image= ForensicAppointmentRequests.objects.get(pk= image_id)
    imageforage= str(get_image.image)
    # print("sadddddddddd" , imageforage)
    imagePath = removeNoise("media/" + imageforage)
    Age1 = estimaeAge(imagePath)
    print("[+] The age of person is with resnet50 is ", Age1 )
    print(f"[+] imagePath is {imagePath}")
    messages.success(request ,imagePath,extra_tags='noise')
    # messages.error(request, Age1 ,extra_tags='noise')
    request.session["Age1"] = Age1  
    return redirect("age_estimation")


@method_decorator(doctor_patient_not_allowed_on_forensic('/'), name='dispatch')
class GeneratePDF(View):
    def get(self, request,image_id, *args, **kwargs, ):
        image_id= int(image_id)
        get_image= ForensicAppointmentRequests.objects.get(pk= image_id)
        
        imageforage= str(get_image.image)
        # Age2 = estimaeAge( "media/" +imageforage)
        data = {
            'PaitentName': get_image.user, 
            'Desc': get_image.desc,
            'Status': get_image.status,
            'Age': request.session["Age1"],
            'Image': get_image.image,
        }
        pdf = render_to_pdf('report/Report.html', data) 
        return HttpResponse(pdf, content_type='application/pdf')


#AGE ESTIMATION FUNCTION WHERE BUTTON IS INCLUDED

@login_required
@doctor_patient_not_allowed_on_forensic('/')
def age_estimation(request):
    AcceptedRequest = ForensicAppointmentRequests.objects.filter(status=True).filter(forensic_agent_id=request.user.id)
    context={ "AcceptedRequest":AcceptedRequest}
    return render(request,"forensic/age-estimation.html", context=context)

@login_required
@doctor_patient_not_allowed_on_forensic('/')
def models(request):
    AcceptedRequest = ForensicAppointmentRequests.objects.filter(status=True).filter(forensic_agent_id=request.user.id)
    context={ "AcceptedRequest":AcceptedRequest}
    return render(request,"forensic/models.html", context=context)

@login_required
@doctor_patient_not_allowed_on_forensic('/')
def svm(request, image_id):
    image_id= int(image_id)
    get_image= ForensicAppointmentRequests.objects.get(pk= image_id)
    imageforage= str(get_image.image)
    print("sadddddddddd" , imageforage)
    Age = SvmMode( "media/" +imageforage)
     
    messages.success(request,mark_safe( "Age with SVM: "+  Age))
    return redirect("models")

@login_required
@doctor_patient_not_allowed_on_forensic('/')
def knn(request, image_id):
    image_id= int(image_id)
    get_image= ForensicAppointmentRequests.objects.get(pk= image_id)
    imageforage= str(get_image.image)
    print("sadddddddddd" , imageforage)
    Age = KnnModel( "media/" +imageforage)
    messages.success(request,mark_safe( "Age with KNN : "+  Age))
    return redirect("models")

@login_required
@doctor_patient_not_allowed_on_forensic('/')
def resnet(request, image_id):
    image_id= int(image_id)
    get_image= ForensicAppointmentRequests.objects.get(pk= image_id)
    imageforage= str(get_image.image)
    print("sadddddddddd" , imageforage)
    Age = estimaeAge( "media/" +imageforage)
    messages.success(request,mark_safe( "Age with Resnet50 : "+  Age))
    return redirect("models")


# from AgeEstimationModel.AgeEstimator import estimaeAge
# def age_estimation_form(request):
#     form = ForensicImageUploadingForm(request.POST, request.FILES)
#     context = {"form":form}
#     if form.is_valid():
#         filename = request.FILES["image"]
#         print("[+]Filename is ", filename.name)
#         form.save()
#         Age = estimaeAge("media\ForensicImages\\"+filename.name)
#         print("[+] The age of person is ", Age )
#     else:
#         print("[+] form is not valid")
#     return render(request,"forensic/age-estimation-form.html", context=context)

#Patient .......................................................................----


@login_required
@doctor_forensic_not_allowed_on_patient('/')
def patient_dashboard(request):
    
    all_appointments = PaitentForensicAppointment.objects.all()
    user_count = DatabaseForPaitentDoctor.objects.filter(user=request.user).count()
    user_count2  = PaitentForensicAppointment.objects.filter(user=request.user).count()
    user_count3  = CustomUser.objects.filter(is_doctor=True).count()
    min_suggestions = DatabaseForPaitentDoctor.objects.filter(user=request.user)[:5]
    min_reports  = PaitentForensicAppointment.objects.filter(user=request.user)[:5]
    context = {
        "all_appointments":all_appointments,
        'user_count' : user_count, 
        'user_count2' : user_count2,
        'user_count3' : user_count3,
        'min_suggestions' :min_suggestions,
        'min_reports' : min_reports
        }
    return render(request,"patient/patient_dashboard.html" , context=context)


@login_required
@doctor_forensic_not_allowed_on_patient('/')
def generate_report(request):
    form = ForensicAppointmentRequestForm(request.POST, request.FILES)
    context = {"form":form}
    if form.is_valid():
        savedForm = form.save(commit=False)
        savedForm.user = request.user
        form.save()
        messages.success(request, "Successfully Sent!")
    return render(request,"patient/generate_report.html",context=context)


@login_required
@doctor_forensic_not_allowed_on_patient('/')
def forensic_appointments(request):
    all_appointments = PaitentForensicAppointment.objects.filter(user=request.user)
    context = {"all_appointments":all_appointments}
    return render(request, "patient/forensic_appointments.html",context=context)


@login_required
@doctor_forensic_not_allowed_on_patient('/')
def doctors_list(request):
    all_objects = CustomUser.objects.filter(is_doctor=True)
    all_location= SomeLocationModel.exportlocation()

    # context = {
    #     "doctor_list" : all_objects,
    #     "doctor_location" : all_location 
    # }
    mylist = zip(all_objects , all_location)
    return render(request, "patient/doctors_list.html",{'list': mylist})


@login_required
@doctor_forensic_not_allowed_on_patient('/')
def doctor_detai(request, doc_id):
    all_objects = CustomUser.objects.filter(is_doctor=True).get(id=doc_id)
    all_location= SomeLocationModel.objects.get(user=doc_id)

    context = {
        'doctor_location' : all_location,
        'doctor' : all_objects,
        
    }
    # # mylist = zip(all_objects , all_location)
    # return render(request, "patient/doctor_detail.html",{'list': mylist})
    # print("[+] Doctor id is " , doc_id)
    # doctor = CustomUser.objects.filter(is_doctor=True).get(id=doc_id)
    # print("[+] Doctor Name is ", doctor.first_name)
    # context = {
    #     "doctor":doctor
    # }

    return render(request, "patient/doctor_detail.html", context=context)

# @login_required
# @doctor_forensic_not_allowed_on_patient('/')
# def get_location(request, doc_id):
#     get_location= SomeLocationModel.objects.get(user=doc_id)
    
    
    
#     form = LocationForm()

#     context = {
#         'mymap' : get_location,
#         'form': form
               
#      }
#     return render(request, "patient/get_location.html" , context=context)
from django.views.generic import UpdateView,View,CreateView,ListView
class get_location(UpdateView):
    model = SomeLocationModel
    form_class= LocationForm
   
    
    template_name = "patient/get_location.html"
    def doctor_detai(self , doc_id):
        all_location= SomeLocationModel.objects.get(user=doc_id)

        context = {
            'mymap' : all_location,
            
        }
        return render(self.request, "patient/get_location.html", context=context)
    # def get_context_data(self, *args, **kwargs):
    #     context = super(get_location, self).get_context_data(*args,**kwargs)
    #     context['myapp'] = SomeLocationModel.objects.get(user = self.request)
    #     return context
    
    
    


@login_required
@doctor_forensic_not_allowed_on_patient('/')
def DoctorAppointmentFormPage(request , doc_id):
    form = DoctorAppointmentRequestForm(request.POST, request.FILES)
    context = {"form":form}
    if form.is_valid():
        saveForm = form.save(commit=False)
        saveForm.user = request.user
        saveForm.doctor_id = doc_id
        form.save()
        messages.success(request, "Successfully Sent!")
    return render(request, "patient/DoctorAppointmentForm.html", context=context)


@login_required
@doctor_forensic_not_allowed_on_patient('/')
def InboxMessages(request, doc_id):
    QuestionForm = QuestionModelForm(request.POST or None)
    # AnsForm = AnswersQuestionModelForm(request.POST or None)
    # answeredQuestion = AnswersQuestionModel.objects.filter(user=request.user).filter(status=True)
    Questions = QuestionModel.objects.filter(status=True).filter(User=request.user).filter(doc_id=doc_id)
    print("[+] Questions ", Questions )
    print("[+] User ", type(request.user.first_name))
    context = {"form":QuestionForm , "Message":Questions}

    if QuestionForm.is_valid():
        saveForm = QuestionForm.save(commit=False)
        saveForm.User = request.user
        saveForm.doc_id = doc_id
        saveForm.Author = request.user.first_name
        QuestionForm.save()

    return render(request, "Messages.html", context=context)




@login_required
def handleMessaageForm(request, qid):
    q = QuestionModel.objects.get(id=qid)
    print(f"[+] question is {q.Question}")
    q.Answers = request.POST["Answers"]
    q.status = True
    q.save()
    print(f"[+] Answer is {q.Answers}")
    print(f"[+] status is {q.status}")
    return redirect("paitentMessage")



@login_required
@doctor_forensic_not_allowed_on_patient('/')
def doctor_suggestions(request):
    all_suggestions = DatabaseForPaitentDoctor.objects.filter(user=request.user) # Model data of  Doctor reports on Dashboard
    print("[+]" , all_suggestions)
    print("[+]", request.user.id)
    all_appointments = PaitentForensicAppointment.objects.all()
    context = {"all_appointments":all_appointments, "all_suggestions":all_suggestions}
    return render(request,"patient/doctor_suggestions.html", context=context)



# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ ForensicAppointmentFormRequestSetction\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def forensicAppointmentView(request):
    return render(request, "hello world")
