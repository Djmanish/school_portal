from django.db import models
from main_app.models import *
# Create your models here.

class Lecture(models.Model):
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE, null=True, related_name="institute_lecture")
    
    class_stage_choices = [('Primary','Primary'),('Middle','Middle'),('Highschool','Highschool')]
    class_stage = models.CharField(max_length=50, choices= class_stage_choices, null=True)
    lecture_name = models.CharField(max_length=100)
    start_time = models.TimeField(null=True,)
    end_time = models.TimeField(null=True , )

    def __str__(self):
        return self.lecture_name





class Schedule(models.Model):
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE, null=True, related_name="schedule_institute")
    Class = models.ForeignKey(to=Classes, on_delete=models.PROTECT, null=True, related_name="schedule_class")
    day_choice = [('Monday','Monday'),('Tuesday','Tuesday'),('Wednesday','Wednesday'),('Thursday','Thursday'),('Friday','Friday'),('Saturday','Saturday')]
    day = models.CharField(max_length=30, choices=day_choice)

    lecture_one = models.ForeignKey(to=Lecture, on_delete=models.PROTECT, related_name="schedule_lecture_one", null=True, blank=True,  )
    subject_lecture_one = models.ForeignKey(to=Subjects, on_delete=models.PROTECT, related_name="subject_lecture_one", null=True, blank=True, )
    subject_teacher_lecture_one = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="subject_teacher_lecture_one",  null=True, blank=True, )

    lecture_two = models.ForeignKey(to=Lecture, on_delete=models.PROTECT, null=True, related_name="schedule_lecture_two", blank=True, default=None )
    subject_lecture_two = models.ForeignKey(to=Subjects, on_delete=models.PROTECT, related_name="subject_lecture_two",  null=True, blank=True, )
    subject_teacher_lecture_two = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="subject_teacher_lecture_two",  null=True , blank=True, )

    lecture_three = models.ForeignKey(to=Lecture, on_delete=models.PROTECT, related_name="schedule_lecture_three",  null=True, blank=True,  default=None )
    subject_lecture_three = models.ForeignKey(to=Subjects, on_delete=models.PROTECT, related_name="subject_lecture_three",  null=True, blank=True, )
    subject_teacher_lecture_three = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="subject_teacher_lecture_three",  null=True, blank=True, )

    lecture_four = models.ForeignKey(to=Lecture, on_delete=models.PROTECT, related_name="schedule_lecture_four",  null=True, blank=True,  default=None )
    subject_lecture_four = models.ForeignKey(to=Subjects, on_delete=models.PROTECT, related_name="subject_lecture_four",  null=True, blank=True, )
    subject_teacher_lecture_four = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="subject_teacher_lecture_four",  null=True, blank=True, )

    lecture_five = models.ForeignKey(to=Lecture, on_delete=models.PROTECT, related_name="schedule_lecture_five",  null=True, blank=True,  default=None )
    subject_lecture_five = models.ForeignKey(to=Subjects, on_delete=models.PROTECT, related_name="subject_lecture_five",  null=True, blank=True, )
    subject_teacher_lecture_five = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="subject_teacher_lecture_five",  null=True, blank=True, )

    lecture_six = models.ForeignKey(to=Lecture, null=True, on_delete=models.PROTECT, related_name="schedule_lecture_six", blank=True,  default=None )
    subject_lecture_six = models.ForeignKey(to=Subjects, null=True, on_delete=models.PROTECT, related_name="subject_lecture_six", blank=True, )
    subject_teacher_lecture_six = models.ForeignKey(to=User, null=True, on_delete=models.PROTECT, related_name="subject_teacher_lecture_six", blank=True, )

    lecture_seven = models.ForeignKey(to=Lecture, null=True, on_delete=models.PROTECT, related_name="schedule_lecture_seven", blank=True,  default=None )
    subject_lecture_seven = models.ForeignKey(to=Subjects, on_delete=models.PROTECT, related_name="subject_lecture_seven", null=True, blank=True, )
    subject_teacher_lecture_seven = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="subject_teacher_lecture_seven",  null=True, blank=True, )

    lecture_eight = models.ForeignKey(to=Lecture, on_delete=models.PROTECT, related_name="schedule_lecture_eight", null=True, blank=True,  default=None )
    subject_lecture_eight = models.ForeignKey(to=Subjects, on_delete=models.PROTECT, related_name="subject_lecture_eight", null=True, blank=True, )
    subject_teacher_lecture_eight = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="subject_teacher_lecture_eight", null=True, blank=True, )
    


    def __str__(self):
        return str(self.institute) +" "+ str(self.Class)     