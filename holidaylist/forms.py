from django.forms import ModelForm
from django import forms
from .models import *

class HolidayUpdateForm(forms.ModelForm):
    class Meta:
        model = HolidayList
        fields = ['date','days','name', 'applicable','holiday_type','holiday_email','holiday_sms','holiday_notification']
        widgets = {
            'date': forms.DateInput(attrs={'type':'date', 'placeholder':'select holiday date'}),
        }