from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import *
from main_app.models import Institute

@receiver(post_save, sender=Institute)
def create_lectures(sender, instance, created, **kwargs):
    if created:
        lectures = ['1st Lecture','2nd Lecture','3rd Lecture','4th Lecture','5th Lecture', '6th Lecture','7th Lecture', '8th Lecture']
        for lecture in lectures:
            Lecture.objects.create(institute=instance, lecture_name= lecture)
        
