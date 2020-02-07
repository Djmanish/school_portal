from django.db import models
from django.contrib.auth.models import User, AbstractUser
from main_app.models import *
from class_schedule.models import *;
from holidaylist.models import *;


# Create your models here.

class ExamType(models.Model):
  institute=models.ForeignKey(to=Institute, on_delete=models.CASCADE, related_name='examtype_institute', null=True)
  exam_type=models.CharField(max_length=100, null=True)
  exam_max_marks=models.CharField(max_length=100, null=True)

  def __str__(self):
    return self.exam_type

  
# class ExamTypeBasicInfo(models.Model):
#    examtype_basicinfo=models.ForeignKey(to=ExamType, on_delete=models.CASCADE, related_name="examtypebasicinfo_institute", null=True)
#    exam_code=models.CharField(max_length=100, null=True)
#    def __str__(self):
#      return self.exam_code

class ExamDetails(models.Model):
  exam_type=models.ForeignKey(to=ExamType, on_delete=models.PROTECT, related_name='exam_type_info', null=True)
  institute=models.ForeignKey(to=Institute, on_delete=models.PROTECT, related_name='examdetails_institute', null=True)
  exam_class=models.ForeignKey(to=Classes, on_delete=models.PROTECT, related_name='examdetails_class', null=True)
  exam_subject=models.CharField(max_length=100, null=True)
  exam_subject_teacher=models.CharField(max_length=100,null=True)
  exam_assign_teacher=models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="exam_assign_teacher", null=True)
  exam_date=models.DateField(max_length=100,null=True,blank=True)
  exam_start_time=models.TimeField(max_length=100, null=True)
  exam_end_time=models.TimeField(max_length=100, null=True)
  
  # class Meta(object):
  #       unique_together = (("exam_subject", "exam_subject_teacher") )

  def __str__(self):
     return self.exam_subject
   