from django.db import models
import datetime
from main_app.models import *

# Create your models here.


class Attendance(models.Model):


   student = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, related_name="student_attendance" )
   # Class_attendance = models.ForeignKey(to=Classes, on_delete=models.PROTECT, null=True, related_name="attendance_class")
  
   
   attendance_status = models.CharField(max_length= 10, null = True)
   # date = models.DateField(null=True)
   date = models.DateField()
   update_date = models.DateTimeField(auto_now=True,null=True)

   def __str__(self):
      return str(self.student)