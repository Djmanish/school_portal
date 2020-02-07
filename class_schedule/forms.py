from django.forms import ModelForm
from django import forms
from .models import *
from main_app.models import *



class Update_lecture_time_Form(ModelForm):
    class Meta:
        model = Lecture
        fields = ['start_time','end_time']

        widgets = {
            'start_time': forms.TimeInput(attrs={'type':'time'}),
            'end_time': forms.TimeInput(attrs={'type':'time'})
        }

