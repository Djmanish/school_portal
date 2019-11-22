from django.forms import ModelForm
from django import forms
from .models import *

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'about', 'profile_pic', 'mobile_number', 'address', 'city', 'state', 'facebook_link']

        widgets = {
            'address': forms.Textarea(attrs={'rows':5, 'placeholder':'Address line 1, Address line 2, city etc...'}),
            'profile_pic': forms.FileInput(),
            'about': forms.Textarea(attrs={'rows':3, 'placeholder':'Tell about yourself in 300 chars'})
           
        }

    