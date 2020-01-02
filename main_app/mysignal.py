from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import *
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance, first_name = instance.username)

@receiver(post_save, sender= UserProfile)
def send_approve_mail(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        if instance.status == 'approve':
            send_mail('Account Approved ',f'Hello {instance.first_name} , Thank you for choosing our application.  ', 'yourcollegeportal@gmail.com',[f'{instance.user.email}'], html_message=f"<h4>Hello {instance.first_name},</h4><p>Your request to join {instance.institute} as {instance.designation} has been approved. Now you can login to your dashboard and update your profile.</p>School Portal<br>school_portal@gmail.com<p></p>"
            )