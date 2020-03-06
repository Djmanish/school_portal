from django.shortcuts import render
from .models import *
import datetime
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def all_notices(request):
    all_notices = Notice.objects.all().order_by('id')
    user_notices = []
    for notice in all_notices:
        notice_recipients = notice.recipients_list.all()
        if request.user.profile in notice_recipients:
            user_notices.insert(0, notice)

    page = request.GET.get('page', 1)
    paginator = Paginator(user_notices, 25)
    try:
        user_notices = paginator.page(page)
    except PageNotAnInteger:
        user_notices = paginator.page(1)
    except EmptyPage:
        user_notices = paginator.page(paginator.num_pages)

    context ={
        'all_notices': user_notices
    }

    return render(request, 'notices/all_notices_list.html', context)



def create_notice(request):
    
    # if request.method == "POST":
    #     subject = request.POST.get('notice_subject')
    #     content = request.POST.get('notice_body')
        
        
    #     new_notice = Notice()
    #     new_notice.institute = request.user.profile.institute
    #     new_notice.subject = subject
    #     new_notice.content = content
    #     new_notice.publish_date = datetime.date.today()
    #     new_notice.save()
    #     if 'send_to_alln' in request.POST:
    #         all_users = UserProfile.objects.all()
    #         for u in all_users:
    #             new_notice.recipients_list.add(u)
    return render(request, 'notices/create_notice.html')



def creating_new_notice(request):
    if request.method == "POST":
        subject = request.POST.get('notice_subject')
        content = request.POST.get('notice_body')
        
        
        new_notice = Notice()
        new_notice.institute = request.user.profile.institute
        new_notice.subject = subject
        new_notice.content = content
        new_notice.publish_date = datetime.date.today()
        new_notice.save()
        recipients_valid_list = []
        print(request.user.user_institute_role.level.level_id)
        all_recipients = Role_Description.objects.filter(institute= request.user.profile.institute)
        for recipient in all_recipients:
            if request.user.user_institute_role.level.level_id <  recipient.level.level_id:
                recipients_valid_list.append(recipient)
        
        for u in recipients_valid_list:
            user_name = u.user.profile
            new_notice.recipients_list.add(user_name)
        






    return HttpResponse('this is from ajax')

            
        
        

    