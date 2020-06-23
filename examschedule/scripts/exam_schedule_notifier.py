from django.core.mail import send_mail
from datetime import timedelta, datetime, date
from examschedule.models import ExamDetails
from main_app.models import UserProfile
from django.utils import timezone
from AddChild.models import AddChild
from notices.models import Notice

def run():
    exams_tomorrow = ExamDetails.objects.filter(exam_date = date.today() + timedelta(days=1))
   
    
    for exam in exams_tomorrow:
        exam_reminder_notice =  Notice.objects.create(institute = exam.institute , category ="Exam Schedule", subject =f"Class {exam.exam_class} exam scheduled on {exam.exam_date}", content=f"Class {exam.exam_class} exam scheduled on {exam.exam_date} at {exam.exam_start_time} for subject {exam.exam_subject}  ", created_at= timezone.now(), publish_date= timezone.now() )

        all_students = UserProfile.objects.filter(Class= exam.exam_class, institute= exam.institute)
        all_parents = AddChild.objects.filter(child__in=all_students, status="active")

        for student in all_students:
            exam_reminder_notice.recipients_list.add(student)
        
        for parent in all_parents:
            exam_reminder_notice.recipients_list.add(parent.parent)



