from django.db import models

# Create your models here.

class ExamResult(models.Model):
    result_institute=models.ForeignKey(to=Institute, on_delete=models.CASCADE, null=True)
    result_class=models.ForeignKey(to=Classes, on_delete=models.CASCADE, null=True)
    result_subject=models.ForeignKey(to=Subjects, on_delete=models.CASCADE, null=True)
    result_subject_teacher=models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    result_max_marks=models.CharField(max_length=100, null=True)
    result_exam_type=models.ForeignKey(to=ExamType, on_delete=models.CASCADE, null=True)
    result_student_first_name=models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    result_student_last_name=models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    result_student_roll_no=models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    result_score=models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.result_subject