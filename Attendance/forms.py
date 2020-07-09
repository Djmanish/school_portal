from django.forms import ModelForm
from main_app.models import UserProfile, Student_Info
from django import forms



class Student_profile_edit_form(ModelForm):

    middle_name = forms.CharField(max_length=25, required=False)

    class Meta:
        model = UserProfile
        exclude = ['user','institute','designation','Class','status','class_promotion_status','class_current_year','class_next_year','created_at','updated_at','qualification']
    
        widgets = {
        'date_of_birth':forms.DateInput(attrs={'type':'date'})
         
           
        }

class Student_info_edit_form(ModelForm):
    f_Email_Id = forms.EmailField()
    class Meta:
        model = Student_Info
        exclude = ['student']

