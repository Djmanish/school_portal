from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
# from django.contrib.auth.models import User
from .models import *
from main_app.models import UserProfile, Institute_levels


@receiver(post_save, sender=Notice)# adding all authority above teacher to receipient list
def save_profile(sender, instance, created, **kwargs):
    if created:
        teacher_level_id = Institute_levels.objects.get(institute= instance.institute ,level_name='teacher')
        all_authorities = UserProfile.objects.filter(institute= instance.institute, designation__level_id__lt = teacher_level_id.level_id)
        for user in all_authorities:
            instance.recipients_list.add(user)



        


