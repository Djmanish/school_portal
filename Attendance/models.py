from django.db import models
import datetime
from main_app.models import *

# Create your models here.


class Attendance(models.Model):


   student = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True, related_name="student_attendance" )
   institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE, related_name='institute_attendance', null=True, blank=True)
   student_class = models.ForeignKey(to=Classes, on_delete=models.CASCADE, related_name="attendance_class", null=True, blank=True) 
   attendance_status = models.CharField(max_length= 10, null = True)
 
   date = models.DateField()
   

   def __str__(self):
      return str(self.student)