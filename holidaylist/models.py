from django.db import models
from main_app.models import *



# Week Days


# Holiday List Model
class HolidayList(models.Model):
   
    DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
    )
    # institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE,related_name='institute_holiday', null=True)
    date=models.DateField(max_length=100, null=True)
    days = models.CharField(max_length=10, choices=DAYS_OF_WEEK, null= True)
    name = models.CharField(max_length=100, null=True)
    applicable =models.CharField(max_length=10,null=True, choices=(('No', 'No'), ('Yes', 'Yes')))
    holiday_type= models.CharField(max_length=100, null=True)
    holiday_email=models.CharField(max_length=10,null=True, choices=(('No', 'No'), ('Yes', 'Yes')))
    holiday_sms=models.CharField(max_length=10,null=True, choices=(('No', 'No'), ('Yes', 'Yes')))
    holiday_notification=models.CharField(max_length=10,null=True, choices=(('No', 'No'), ('Yes', 'Yes')))
    created_at= models.DateTimeField(auto_now=True, null=True, )
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
 
    def __str__(self):
            return str(self.name)    


class SendEmail(models.Model):
    mail_to=models.CharField(max_length=1000)
    mail_subject=models.CharField(max_length=1000)
    mail_content = models.CharField(max_length=1000)
    # mail_from = models.CharField(max_length=1000)
    mail_date=models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.mail_to)