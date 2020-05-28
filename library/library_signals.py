from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from .models import *
from main_app.models import Institute
from notices.models import *
from django.contrib.auth.signals import user_logged_in


# starting signal for creating library notification category when institute is created
@receiver(post_save, sender=Institute)
def LibraryNoticeCategory(sender, instance, created, **kwargs):
    if created:
        try:
            Notification_Category.objects.get(name="Library", institute= instance)
        except:
            Notification_Category.objects.create(name="Library", institute= instance)
# ending signal for creating library notification category when institute is created

# starting sending notification when Book Issued
@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    if request.user.profile.designation.level_name == "admin":
        last_log = request.user.last_login.date()
        today = timezone.now().date()
        print(today)
    else:
        print('...do your stuff..')
    
@receiver(post_save, sender=IssueBook)
def issue_book_notification(sender, instance, created, **kwargs):
    if created:

        try:
            library_category = Notification_Category.objects.get(institute=instance.issue_book_institute, name="Library")
        except:
            library_category=None
        libray_issuebook_notice= Notice.objects.create(institute = instance.issue_book_institute, category =library_category, subject =f"New Book Issued Book Name-{instance.book_name.book_name}", content=f"{instance.book_name.book_name} with book ID-{instance.book_name.book_id} is issued to your account ", created_at= timezone.now(), publish_date= timezone.now() )
        libray_issuebook_notice.recipients_list.add(instance.user_name)
    # ending sending notification when Book Issued
    # starting sending notification when book is returned
    else:
        if instance.return_date:
            try:
                library_category = Notification_Category.objects.get(institute=instance.issue_book_institute, name="Library")
            except:
                library_category=None
            libray_issuebook_notice= Notice.objects.create(institute = instance.issue_book_institute, category =library_category, subject =f"Book Name-{instance.book_name.book_name} is returned", content=f"{instance.book_name.book_name} with book ID-{instance.book_name.book_id} is returned by your account ", created_at= timezone.now(), publish_date= timezone.now() )
            libray_issuebook_notice.recipients_list.add(instance.user_name)
    # ending sending notification when book is returned
        