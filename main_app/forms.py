from django.forms import ModelForm
from django import forms
from .models import *

    
# class SubjectUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Subjects
#         fields = ['subject_class','subject_code','subject_name']

class ClassUpdateForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = ['name','class_stage','class_teacher']
    



class InstituteUpdateProfile(forms.ModelForm):
    class Meta:
        model = Institute
        fields = ['code','name','establish_date', 'session_start_date', 'profile_pic','principal','about','contact_number1','contact_number2','contact_number3','address1','address2','district','state','country','pin_code','email','facebook_link','website_link']

        widgets = {
            'establish_date': forms.DateInput(attrs={'type':'date'}),
            'session_start_date' : forms.DateInput(attrs={'type':'date','required':'required'}),
            'profile_pic': forms.FileInput()

        }

