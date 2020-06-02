# from django.core.mail import send_mail
from library.models import *
from django.utils import timezone
from datetime import timedelta
from notices.models import *
from AddChild.models import *

def run():  
    today= timezone.now().date()    
    chk= IssueBook.objects.filter(return_date__isnull=True) 
    for c in chk:
        chk_days = c.issue_book_institute.library_settings.send_Reminder_Before
        for i in range(chk_days):
            delta= c.expiry_date-timedelta(days=i)
            print(delta)
            if delta.date() == today:
                print("if running")
                libray_issuebook_notice= Notice.objects.create(institute = c.issue_book_institute, category ='Library', subject =f"Book Name: {c.book_name.book_name} Due Date Is {c.expiry_date}", content=f"Your Issued Book Name: {c.book_name.book_name} Due Date Is {c.expiry_date}. Please Returned It Before The Due Date", created_at= timezone.now(), publish_date= timezone.now())


                libray_issuebook_notice.recipients_list.add(c.user_name)
                try:
                    student_parent= AddChild.objects.filter(child= c.user_name).first()
                    libray_issuebook_notice.recipients_list.add(student_parent.parent)
                except:
                    pass




    # for i in chk:
    #     date_prev = i.expiry_date-timedelta(days=2)
    #     date_prev2 = i.expiry_date-timedelta(days=1)
    #     ex= i.expiry_date.date()
    #     if date_prev.date() == today:
    #         libray_issuebook_notice= Notice.objects.create(institute = i.issue_book_institute, category ='Library', subject =f"Your Issued Book Name: {i.book_name.book_name} Due Date Is {ex}", content=f"Your Issued Book Name: {i.book_name.book_name} Due Date Is {ex}. Please Returned It Before The Due Date", created_at= timezone.now(), publish_date= timezone.now() )
    #         libray_issuebook_notice.recipients_list.add(i.user_name)
    #     elif date_prev2.date() == today:
    #         libray_issuebook_notice= Notice.objects.create(institute = i.issue_book_institute, category ='Library', subject =f"Your Issued Book Name: {i.book_name.book_name} Due Date Is {ex}", content=f"Your Issued Book Name: {i.book_name.book_name} Due Date Is {ex}. Please Returned It Before The Due Date", created_at= timezone.now(), publish_date= timezone.now() )
    #         libray_issuebook_notice.recipients_list.add(i.user_name)
    #     elif (i.expiry_date).date == today:
    #         libray_issuebook_notice= Notice.objects.create(institute = i.issue_book_institute, category ='Library', subject =f"Your Issued Book Name: {i.book_name.book_name} Due Date Is {ex}", content=f"Your Issued Book Name: {i.book_name.book_name} Due Date Is {ex}. Please Returned It Before The Due Date", created_at= timezone.now(), publish_date= timezone.now() )
        
        
        



