from django.forms import ModelForm
from django import forms
from .models import *
from django.core.exceptions import NON_FIELD_ERRORS

class Fees_tag_update_form(forms.ModelForm):
    class Meta:
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
        model = School_tags
        fields = ['fees_code','description','type','active','amount','tax_percentage','start_date','end_date']

        widgets = {
             'fees_code': forms.TextInput(attrs={'readonly':'readonly'}),
            'description': forms.TextInput(attrs={'row':'2'}),
            'start_date':forms.TextInput(attrs={'type':'date'}),
            'end_date':forms.TextInput(attrs={'type':'date'}),
            'amount':forms.TextInput(attrs={'class':'only_decimal'}),
            'tax_percentage':forms.TextInput(attrs={'class':'only_decimal'})
        }
        
        def clean(self): 
  
            # data from the form is fetched using super function 
            super(Fees_tag_update_form, self).clean() 
            
            # extract the username and text field from the data 
            fees_code = self.cleaned_data.get('fees_code') 
            existing_fees_code = School_tags.objects.get(fees_code= fees_code)
            if fees_code:
                self._errors['fees_code']= self.error_class(['Tag with this fees code already exists !!!'])
    
            
    
            # return any errors if found 
            return self.cleaned_data

                

        
