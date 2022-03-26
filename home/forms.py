from django import forms
from .models import contact




#DataFlair
class Contact(forms.ModelForm):
    class Meta:
        model = contact
        fields = '__all__'
        widgets = {
           'name': forms.TextInput(attrs={'placeholder': "Full Name"}),
           'email': forms.TextInput(attrs={'placeholder': "Email"}),
           'message': forms.Textarea(attrs={'placeholder': "Description"})

        }
       

