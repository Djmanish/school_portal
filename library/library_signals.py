from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from .models import *
from main_app.models import Institute
from notices.models import *
from django.contrib.auth.signals import user_logged_in


# starting signal for creating library settings when institute is created
@receiver(post_save, sender=Institute)
def LibrarySetting(sender, instance, created, **kwargs):
    if created:
        LibrarySettings.objects.create(institute=instance, max_Book_Allows= 3, day_Span= 5, send_Reminder_Before= 2)
# ending signal for creating library settings when institute is created

# starting sending notification when Book Issued    
@receiver(post_save, sender=IssueBook)
def issue_book_notification(sender, instance, created, **kwargs):
    if created:
        libray_issuebook_notice= Notice.objects.create(institute = instance.issue_book_institute, category ='Library', subject =f"New Book Issued Book Name-{instance.book_name.book_name}", content=f"{instance.book_name.book_name} with book ID-{instance.book_name.book_id} is issued to your account ", created_at= timezone.now(), publish_date= timezone.now() )
        libray_issuebook_notice.recipients_list.add(instance.user_name)
    # ending sending notification when Book Issued
    # starting sending notification when book is returned
    else:
        if instance.return_date:
            libray_issuebook_notice= Notice.objects.create(institute = instance.issue_book_institute, category ='Library', subject =f"Book Name-{instance.book_name.book_name} is returned", content=f"{instance.book_name.book_name} with book ID-{instance.book_name.book_id} is returned by your account ", created_at= timezone.now(), publish_date= timezone.now() )
            libray_issuebook_notice.recipients_list.add(instance.user_name)
    # ending sending notification when book is returned
        