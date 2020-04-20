from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import *
from django.core.mail import send_mail


# signal for creating fees summary automatic
@receiver(post_save, sender=Student_Tag_Processed_Record)
def create_summary(sender, instance, created, **kwargs):
    if created:
        try:
            # if student already exist for this due date
            student = Students_fees_table.objects.get( institute= instance.institute, student= instance.student, due_date= instance.due_date)
            student.total_due_amount = student.total_due_amount + instance.amount_including_tax
            student.save()
        except:
            #creating a new student if does not exist
            new_student = Students_fees_table.objects.create(institute= instance.institute,student= instance.student, due_date= instance.due_date)
            new_student.total_due_amount = new_student.total_due_amount + instance.amount_including_tax
            new_student.save()

