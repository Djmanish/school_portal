from django.forms import ModelForm
from django import forms

from .models import *
from PIL import Image
from datetime import date
from django.core.exceptions import ValidationError


    
# class SubjectUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Subjects
#         fields = ['subject_class','subject_code','subject_name']



class ClassUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Classes
        fields = ['name','class_stage','class_teacher']
    



class InstituteUpdateProfile(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(InstituteUpdateProfile, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['code'].required = True
        self.fields['establish_date'].required = True
        self.fields['session_start_date'].required = True
        self.fields['address2'].required = False
        self.fields['state'].required = True
        self.fields['country'].required = True
        self.fields['pin_code'].required = True
  

    class Meta:
        model = Institute
        fields = ['code','name','establish_date', 'session_start_date', 'profile_pic','institute_logo', 'principal','about','contact_number1','contact_number2','contact_number3','address1','address2','district','state','country','pin_code','email','facebook_link','website_link']

        widgets = {
            'establish_date': forms.DateInput(attrs={'type':'date'}),
            'session_start_date' : forms.DateInput(attrs={'type':'date','required':'required'}),
            'profile_pic': forms.FileInput(),
            'institute_logo': forms.FileInput(),
            'about':forms.Textarea(attrs={'rows':3}),
            'contact_number1':forms.TextInput(attrs={'class':'positive_number'}),
            'contact_number2':forms.TextInput(attrs={'class':'positive_number'}),
            'contact_number3':forms.TextInput(attrs={'class':'positive_number'}),
            
       
        }
       

       

        labels = {
        'profile_pic': 'Profile Picture',
        'code':'School Code',
        'name':'School Name',
        'establish_date':'Establish Date',
        'session_start_date':'Session Start Date',
        'contact_number1':'Contact No. 1',
        'contact_number2':'Contact No. 2',
        'contact_number3':'Contact No. 3',
        'address1':'Address Line 1',
        'address2':'Address Line 2',
        'pin_code':'Pin Code',
        'facebook_link':'Facebook Link',
        'website_link':'School Website Link',
        'district':'City',
        'institute_logo': 'Institute Logo',

    }

            
            
            

       
