from django.forms import ModelForm
from django import forms
from .models import *

class HolidayUpdateForm(forms.ModelForm):
    class Meta:
        model = HolidayList
        fields = ['date','days','name', 'applicable','holiday_type','holiday_email','holiday_sms','holiday_notification']
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
        }


class ContactForm(forms.Form):
    to_email = forms.EmailField(required=True)
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    