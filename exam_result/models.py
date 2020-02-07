from django.db import models
from main_app.models import *
from examschedule.models import *

# Create your models here.

class ExamResult(models.Model):
    institute=models.ForeignKey(to=Institute, on_delete=models.CASCADE,related_name='result_institute', null=True)
    result_class=models.ForeignKey(to=Classes, on_delete=models.CASCADE,related_name='result_class', null=True)
    result_subject=models.ForeignKey(to=Subjects, on_delete=models.CASCADE,related_name='result_subject', null=True)
    result_subject_teacher=models.ForeignKey(to=User, on_delete=models.CASCADE,related_name='result_subject_teacher', null=True)
    result_max_marks=models.CharField(max_length=100, null=True)
    result_exam_type=models.ForeignKey(to=ExamType, on_delete=models.CASCADE,related_name='result_exam_type', null=True)
    result_student_data=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='result_student_data',null=True)
    # result_student_last_name=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='result_student_last_name', null=True)
    # result_student_roll_no=models.ForeignKey(to=UserProfile, on_delete=models.CASCADE,related_name='result_student_roll_no', null=True)
    result_score=models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.result_student_data)


class ExamView(models.Model):
    institute=models.ForeignKey(to=Institute, on_delete=models.CASCADE,related_name='examview_institute', null=True)
    examview_class=models.ForeignKey(to=Classes, on_delete=models.CASCADE,related_name='examview_class', null=True)
    examview_subject=models.ForeignKey(to=Subjects, on_delete=models.CASCADE,related_name='examview_subject', null=True)
    examview_max_marks=models.CharField(max_length=100, null=True)
    examview_type=models.ForeignKey(to=ExamType, on_delete=models.CASCADE,related_name='examview_type', null=True)
    examview_final_score_per=models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.examview_type)