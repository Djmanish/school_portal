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
    test_subject_one=models.ForeignKey(to=Subjects, on_delete=models.CASCADE, related_name='test_subject_one', null=True,blank=True)
    test_date_one=models.DateField(max_length=100,null=True)
    test_time_one=models.TimeField(max_length=100,null= True)
    subject_teacher_one=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='subject_teacher_one', null=True,blank=True)
    assign_teacher_one=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='assign_teacher_one', null=True,blank=True)
    test_subject_two=models.ForeignKey(to=Subjects, on_delete=models.CASCADE, related_name='test_subject_two', null=True,blank=True)
    test_date_two=models.DateField(max_length=100,null=True)
    test_time_two=models.TimeField(max_length=100,null= True)
    subject_teacher_two=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='subject_teacher_two', null=True,blank=True)
    assign_teacher_two=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='assign_teacher_two', null=True,blank=True)
    test_subject_three=models.ForeignKey(to=Subjects, on_delete=models.CASCADE, related_name='test_subject_three', null=True,blank=True)
    test_date_three=models.DateField(max_length=100,null=True)
    test_time_three=models.TimeField(max_length=100,null= True)
    subject_teacher_three=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='subject_teacher_three', null=True,blank=True)
    assign_teacher_three=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='assign_teacher_three', null=True,blank=True)
    test_subject_four=models.ForeignKey(to=Subjects, on_delete=models.CASCADE, related_name='test_subject_four', null=True,blank=True)
    test_date_four=models.DateField(max_length=100,null=True)
    test_time_four=models.TimeField(max_length=100,null= True)
    subject_teacher_four=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='subject_teacher_four', null=True,blank=True)
    assign_teacher_four=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='assign_teacher_four', null=True,blank=True)
    test_subject_five=models.ForeignKey(to=Subjects, on_delete=models.CASCADE, related_name='test_subject_five', null=True,blank=True)
    test_date_five=models.DateField(max_length=100,null=True)
    test_time_five=models.TimeField(max_length=100,null= True)
    subject_teacher_five=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='subject_teacher_five', null=True,blank=True)
    assign_teacher_five=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='assign_teacher_five', null=True,blank=True)
    test_subject_six=models.ForeignKey(to=Subjects, on_delete=models.CASCADE, related_name='test_subject_six', null=True,blank=True)
    test_date_six=models.DateField(max_length=100,null=True)
    test_time_six=models.TimeField(max_length=100,null= True)
    subject_teacher_six=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='subject_teacher_six', null=True,blank=True)
    assign_teacher_six=models.ForeignKey(to=Schedule, on_delete=models.CASCADE,related_name='assign_teacher_six', null=True,blank=True)

    def __str__(self):
      return self.test_code

