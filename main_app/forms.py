from django.forms import ModelForm
from django import forms
from .models import *

    
class SubjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = ['subject_class','subject_code','subject_name']
       