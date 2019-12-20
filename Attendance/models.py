from django.db import models
from main_app.models import *

# Create your models here.


class Attendance(models.Model):
   Ds = [
      ('present','Present'),('absent','Absent'),('leave','Leave'),('holiday','Holiday'),
   ]  
   institute =models.ForeignKey(to=Institute, on_delete=models.CASCADE, related_name='institue_name')  
   classes =models.ForeignKey(to=Classes, on_delete=models.CASCADE, related_name='classes')
   rollno = models.CharField(max_length=25, null=True, default="")
   first_name = models.CharField(max_length=25, null=True, default="")     
   last_name = models.CharField(max_length= 25, null = True,default="")
   attendance_status = models.CharField(max_length= 100, null = True,default="")
   current_date = models.DateTimeField(auto_now_add=True,null=True)
   daily_status = models.CharField(max_length=25,choices=Ds,default="--Select--")

   def __str__(self):
      return str(self.first_name)