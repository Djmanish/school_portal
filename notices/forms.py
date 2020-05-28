from django.forms import ModelForm
from .models import Notice
from django import forms
class NoticeUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(NoticeUpdateForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['content'].required = True
        self.fields['subject'].required = True
    
    class Meta:
        model = Notice
        fields = ['subject','content',]

        widgets = {
           
            'content' : forms.Textarea(attrs={'rows':'3'}),
        
          

        }