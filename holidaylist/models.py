from django.db import models
from main_app.models import *


# Week Days
Answers=[
    ('yes', 'yes'),
    ('no','no'),
],
DAYS_OF_WEEK = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]

# Holiday List Model
class HolidayList(models.Model):
    # institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE,related_name='institute_holiday', null=True)
    date=models.DateField(max_length=100, null=True)
    days = models.CharField(max_length=10, choices=DAYS_OF_WEEK, null= True)
    name = models.CharField(max_length=100, null=True)
    applicable =models.CharField(max_length=10,choices=Answers, null=True, default="Yes")
    holiday_type= models.CharField(max_length=100, null=True)
    holiday_email=models.CharField(max_length=10,choices=Answers, null=True, default="No")
    holiday_sms=models.CharField(max_length=10, choices=Answers,null=True, default="No")
    holiday_notification=models.CharField(max_length=10, choices=Answers, null=True, default="No")
    created_at= models.DateTimeField(auto_now=True, null=True, )
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def yes(self):
        self.status= 'yes'
        self.save()
    def no(self):
        self.status= 'no'
        self.save()
    def __str__(self):
            return str(self.name)    