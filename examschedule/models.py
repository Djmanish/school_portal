from django.db import models
from django.contrib.auth.models import User, AbstractUser
from main_app.models import *
from class_schedule.models import *;
from holidaylist.models import *;


# Create your models here.

class ExamSchedule(models.Model):
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE,related_name='examschedule', null=True)
    test_code=models.CharField(max_length=100, null=True)
    test_class=models.ForeignKey(to=Classes, on_delete=models.CASCADE,related_name='test_class', null=True)
    test_type_choices= [('Unit','Unit'),('Half Yearly','Half Yearly'),('Yearly','Yearly')]
    test_type = models.CharField(max_length=50, choices= test_type_choices, null=True)
    test_subject1=models.ForeignKey(to=Subjects, on_delete=models.CASCADE, related_name='test_subject_one', null=True,blank=True)
    test_date1=models.DateField(max_length=100,null=True)
    test_time1=models.TimeField(max_length=100,null= True)
    subject_teacher1=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='subject_teacher_one', null=True,blank=True)
    assign_teacher1=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='assign_teacher_one', null=True,blank=True)
    test_subject2=models.ForeignKey(to=Subjects, on_delete=models.CASCADE, related_name='test_subject_two', null=True,blank=True)
    test_date2=models.DateField(max_length=100,null=True)
    test_time2=models.TimeField(max_length=100,null= True)
    subject_teacher2=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='subject_teacher_two', null=True,blank=True)
    assign_teacher2=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='assign_teacher_two', null=True,blank=True)
    test_subject3=models.ForeignKey(to=Subjects, on_delete=models.CASCADE, related_name='test_subject_three', null=True,blank=True)
    test_date3=models.DateField(max_length=100,null=True)
    test_time3=models.TimeField(max_length=100,null= True)
    subject_teacher3=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='subject_teacher_three', null=True,blank=True)
    assign_teacher3=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='assign_teacher_three', null=True,blank=True)
    test_subject4=models.ForeignKey(to=Subjects, on_delete=models.CASCADE, related_name='test_subject_four', null=True,blank=True)
    test_date4=models.DateField(max_length=100,null=True)
    test_time4=models.TimeField(max_length=100,null= True)
    subject_teacher4=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='subject_teacher_four', null=True,blank=True)
    assign_teacher4=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='assign_teacher_four', null=True,blank=True)
    test_subject5=models.ForeignKey(to=Subjects, on_delete=models.CASCADE, related_name='test_subject_five', null=True,blank=True)
    test_date5=models.DateField(max_length=100,null=True)
    test_time5=models.TimeField(max_length=100,null= True)
    subject_teacher5=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='subject_teacher_five', null=True,blank=True)
    assign_teacher5=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='assign_teacher_five', null=True,blank=True)
    test_subject6=models.ForeignKey(to=Subjects, on_delete=models.CASCADE, related_name='test_subject_six', null=True,blank=True)
    test_date6=models.DateField(max_length=100,null=True)
    test_time6=models.TimeField(max_length=100,null= True)
    subject_teacher6=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='subject_teacher_six', null=True,blank=True)
    assign_teacher6=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='assign_teacher_six', null=True,blank=True)

    def __str__(self):
      return self.test_code

