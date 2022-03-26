from django import forms
from .models import PatientRecord
from .models import ForensicImageRecord



#DataFlair
class PatientCreate(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = '__all__'
 


class ForensicImageUploadingForm(forms.ModelForm):
    class Meta:
        model = ForensicImageRecord
        fields = '__all__'

from .models import ForensicAppointmentRequests

class ForensicAppointmentRequestForm(forms.ModelForm):
    class Meta:
        model = ForensicAppointmentRequests
        fields = ["image", "desc"]
        labels = {
        "image": "X-RAY Image",
        "desc": "Description",

        }

from .models import AppointmentDoctorModel
class DoctorAppointmentRequestForm(forms.ModelForm):
    class Meta:
        model = AppointmentDoctorModel
        fields = ["desc", "report"]


from .models import PaitentForensicAppointment
class PaitentForensicAppointmentForm(forms.ModelForm):
    class Meta:
        model = PaitentForensicAppointment
        fields = ['desc', 'flie']


from .models import DatabaseForPaitentDoctor
class DatabaseForPaitentDoctorForm(forms.ModelForm):
    class Meta:
        model = DatabaseForPaitentDoctor
        fields = ["suggestions", "flie"]