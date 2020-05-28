from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from .models import *
from django.core.mail import send_mail
import datetime
from datetime import timedelta
from notices.models import *
from django.utils import timezone
from main_app.models import Institute
from AddChild.models import *


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

# starting signal for creating fees notification category when institute is created
# @receiver(post_save, sender=Institute)
# def FessNoticeCategory(sender, instance, created, **kwargs):
#     if created:
#         try:
#             Notification_Category.objects.get(name="Fees", institute= instance)
#         except:
#             Notification_Category.objects.create(name="Fees", institute= instance)
# ending signal for creating fees notification category when institute is created
            
# starting signal for creating notification for fees due date
@receiver(post_save, sender=Fees_Schedule)
def due_date_notification(sender, instance, created, **kwargs):
    if created:
      
        due_notice = Notice.objects.create(institute = instance.institute, category='Fees', subject =f"Fees for the due date {instance.due_date} available", content=f"Your institute has updated Due Date. Now fees for {instance.due_date} is available. You can pay now.", created_at= timezone.now(), publish_date= instance.notification_date )
        
        all_parents = UserProfile.objects.filter(institute= instance.institute, designation__level_name= 'parent' )
        for p in all_parents:
            due_notice.recipients_list.add(p)
        all_students = UserProfile.objects.filter(institute= instance.institute, designation__level_name= 'student')
        for s in all_students:
            due_notice.recipients_list.add(s)
    else:
        due_notice = Notice.objects.create(institute = instance.institute, category='Fees', subject =f"Fees for the due date {instance.due_date} available", content=f"Your institute has updated Due Date. Now fees for {instance.due_date} is available. You can pay now.", created_at= timezone.now(), publish_date= instance.notification_date )
        
        all_parents = UserProfile.objects.filter(institute= instance.institute, designation__level_name= 'parent' )
        for p in all_parents:
            due_notice.recipients_list.add(p)
        all_students = UserProfile.objects.filter(institute= instance.institute, designation__level_name= 'student')
        for s in all_students:
            due_notice.recipients_list.add(s)

# ending signal for creating notification for fees due date

# starting sending notification if a students tag changed
@receiver(m2m_changed, sender=Student_Tags_Record.tags.through)
def student_tag_changed(sender, instance, action,pk_set, **kwargs):
    if action =='post_add':
        
        all_tags = instance.tags.all()
        tag_str =''
        for t in all_tags:
            tag_str = tag_str + str(t.description)+", "
        
        added_tags=''
        # fetching added tags
        for i in pk_set:
            added_tag= School_tags.objects.get(pk=i)
            added_tags = added_tags+ added_tag.description+", "



        tag_change_notice = Notice.objects.create(institute = instance.institute, category='Fees', subject =f"{instance.student.first_name} {instance.student.last_name}'s fees tags have been changed.", content=f"{instance.student.first_name} {instance.student.last_name}'s fees tags have been changed. Added tag is {added_tags} Currently you are mapped with these tags: {tag_str}", created_at= timezone.now(), publish_date= timezone.now() )

        student = UserProfile.objects.get(pk=instance.student.id)
        tag_change_notice.recipients_list.add(student)

        student_parent= AddChild.objects.filter(child= instance.student).first()
        tag_change_notice.recipients_list.add(student_parent.parent)

    elif action =='post_remove':
 
        all_tags = instance.tags.all()
        tag_str =''
        for t in all_tags:
            tag_str = tag_str + str(t.description)+", "
        
        removed_tags=''
        # fetching removed tags
        for i in pk_set:
            removed_tag= School_tags.objects.get(pk=i)
            removed_tags = removed_tags+ removed_tag.description+", "
        
        tag_change_notice = Notice.objects.create(institute = instance.institute, category="Fees", subject =f"{instance.student.first_name} {instance.student.last_name}'s fees tags have been changed.", content=f"{instance.student.first_name} {instance.student.last_name}'s fees tags have been changed. Removed tag is {removed_tags} Currently you are mapped with these tags: {tag_str}", created_at= timezone.now(), publish_date= timezone.now() )

        student = UserProfile.objects.get(pk=instance.student.id)
        tag_change_notice.recipients_list.add(student)

        student_parent= AddChild.objects.filter(child= instance.student).first()
        tag_change_notice.recipients_list.add(student_parent.parent)

# ending sending notification if a students tag changed


# starting sending notification when fees paid
@receiver(post_save, sender=Students_fees_table)
def fees_paid_notification(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        if instance.total_due_amount <= 0:
           
            fees_paid_notice = Notice.objects.create(institute = instance.institute, category="Fees", subject =f"{instance.student.first_name}'s Fees paid for {instance.due_date}", content=f"{instance.student.first_name}'s Fees paid for {instance.due_date}. Invoice No. is {instance.invoice_number} ", created_at= timezone.now(), publish_date= timezone.now() )
            student = UserProfile.objects.get(pk=instance.student.id)
            fees_paid_notice.recipients_list.add(student)

            student_parent= AddChild.objects.filter(child= instance.student).first()
            fees_paid_notice.recipients_list.add(student_parent.parent)
                

# ending sending notification when fees paid