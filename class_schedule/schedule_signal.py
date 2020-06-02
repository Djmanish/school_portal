from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import *
from main_app.models import Institute, Classes
from notices.models import Notice
from django.utils import timezone

@receiver(post_save, sender=Institute)
def create_lectures(sender, instance, created, **kwargs):
    if created:
        class_stages = ['Primary','Middle','Highschool']
        lectures = ['1st Lecture','2nd Lecture','3rd Lecture','4th Lecture','5th Lecture', '6th Lecture','7th Lecture', '8th Lecture']
        
        for stage in class_stages:
            for lecture in lectures:
                Lecture.objects.create(institute=instance,class_stage= stage, lecture_name= lecture)

# @receiver(post_save, sender=Classes)
# def create_schedule_days(sender, instance, created, **kwargs):
#     if created:
#         days=['Monday','Tuesday', 'Wednesday', 'Thursday','Friday','Saturday']
#         for day in days:
#   
#           create_schedule = Schedule.objects.create(institute=instance.institute, Class= instance, day= day )

# starting sending notification when schedule is updated      
@receiver(post_save, sender=Schedule)
def schedule_update_notice(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        schedule_update_notification = Notice.objects.create(institute = instance.institute, category="Class Schedule", subject =f"{instance.Class} schedule updated ", content=f"{instance.Class} schedule has been updated. Check your updated schedule.  ", created_at= timezone.now(), publish_date= timezone.now() )
        all_students = UserProfile.objects.filter(Class=instance.Class, institute=instance.institute )
        for s in all_students:
            schedule_update_notification.recipients_list.add(s)
# ending sending notification when schedule is updated