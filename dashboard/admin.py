from django.contrib import admin
from .models import PatientRecord
from .models import ForensicImageRecord
from .models import ForensicAppointmentRequests
from .models import PaitentForensicAppointment,DatabaseForPaitentDoctor
# Register your models here.

admin.site.register(PatientRecord)
admin.site.register(ForensicImageRecord)
admin.site.register(ForensicAppointmentRequests)
# admin.site.register(AppointmentRequestDoctor)
admin.site.register(PaitentForensicAppointment)
admin.site.register(DatabaseForPaitentDoctor)
from .models import AppointmentDoctorModel
admin.site.register(AppointmentDoctorModel)