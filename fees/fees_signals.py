from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import *
from django.core.mail import send_mail
import datetime
from datetime import timedelta
from notices.models import *
from django.utils import timezone


# signal for creating fees summary automatic
@receiver(post_save, sender=Student_Tag_Processed_Record)
def create_summary(sender, instance, created, **kwargs):
    if created:
        try:
            #creating a new student if does not exist
            new_student = Students_fees_table.objects.create(institute= instance.institute,student= instance.student, student_class = instance.student.Class , due_date= instance.due_date, )
            new_student.total_due_amount = new_student.total_due_amount + instance.amount_including_tax
            new_student.balance = new_student.total_due_amount# can be deleted

            # invoice number syntax
            
            new_student.invoice_number = (str(instance.institute.id)+"-"+str(instance.student.id)+"-"+str(instance.due_date.strftime("%Y-%d-%m"))).strip() 
            new_student.save()
        except:
            # if student already exist for this due date
            student = Students_fees_table.objects.get( institute= instance.institute, student= instance.student, due_date= instance.due_date)
            student.total_due_amount = student.total_due_amount + instance.amount_including_tax
            student.balance = student.total_due_amount # can be deleted
            student.save()
        
            
# starting signal for creating notification for fees due date
@receiver(post_save, sender=Fees_Schedule)
def due_date_notification(sender, instance, created, **kwargs):
    if created:
        due_notice = Notice.objects.create(institute = instance.institute, subject ="New Fees Due Date Updated", content=f"Institute has updated Due Date. Now fees for {instance.due_date} is available. You can pay now", publish_date= instance.notification_date )
        
        all_parents = UserProfile.objects.filter(institute= instance.institute, designation__level_name= 'parent' )
        for p in all_parents:
            due_notice.recipients_list.add(p)
    else:
        due_notice = Notice.objects.create(institute = instance.institute, subject ="New Fees Due Date Updated", content=f"Institute has updated Due Date. Now fees for {instance.due_date} is available. You can pay now", publish_date=instance.notification_date)
        all_parents = UserProfile.objects.filter(institute= instance.institute, designation__level_name= 'parent' )
        for p in all_parents:
            due_notice.recipients_list.add(p)


# ending signal for creating notification for fees due date