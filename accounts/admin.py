from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser,Doctor,Patient,Forensic
from django.conf import settings
from mapbox_location_field.admin import MapAdmin  
from .models import SomeLocationModel  
from .models import QuestionModel
# Register your models here.
class UserAdmin( admin.ModelAdmin):
    model = CustomUser
    fields = ["is_approve", "is_active"]
class DoctorAdmin( admin.ModelAdmin):
    model = Doctor
    fields = ["Certificate"]
class ForensicAdmin( admin.ModelAdmin):
    model = Forensic
    fields = ["Certificate"]

admin.site.register(CustomUser, UserAdmin )
admin.site.register(Doctor,DoctorAdmin  )
admin.site.register(Patient)
admin.site.register(Forensic,ForensicAdmin )
admin.site.register(SomeLocationModel, MapAdmin)
# admin.site.register(AnswersQuestionModel)
admin.site.register(QuestionModel)

