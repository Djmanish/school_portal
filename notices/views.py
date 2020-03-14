from django.shortcuts import render, redirect
from .models import *
import datetime
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from AddChild.models import *
from django.contrib import messages
# Create your views here.

def all_notices(request):
    teacher_role_level = Institute_levels.objects.get(level_name='teacher', institute= request.user.profile.institute)
    teacher_role_level = teacher_role_level.level_id
    

    user_role_level = request.user.profile.designation.level_id
    



    all_notices = Notice.objects.all().order_by('id')
    user_notices = []
    if user_role_level < teacher_role_level:
        user_notices = all_notices.reverse()
    else:
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
    if request.user.user_institute_role.level.level_name == 'student' or request.user.user_institute_role.level.level_name == 'parent':
        messages.info(request, 'You might not have permission to create a notice !!!')
        return redirect('not_found')
    else:

        user_notices = Notice.objects.filter(author= request.user).order_by('-publish_date')
        author_classes=[]
        if request.user.user_institute_role.level.level_name == 'teacher':
            teacher_classes = Subjects.objects.filter(subject_teacher= request.user)
            for aclass in teacher_classes:
                
                author_classes.append(aclass.subject_class)
        else:
            author_classes = Classes.objects.filter(institute= request.user.profile.institute)

        page = request.GET.get('page', 1)
        paginator = Paginator(user_notices, 20)
        try:
            user_notices = paginator.page(page)
        except PageNotAnInteger:
            user_notices = paginator.page(1)
        except EmptyPage:
            user_notices = paginator.page(paginator.num_pages)

        if request.method == "POST":
            subject = request.POST.get('notice_subject')
            content = request.POST.get('notice_body')
            selected_class = request.POST.get('notice_class')
            notice_refrence_no = request.POST.get('notice_refrence_no').strip()
            try:
                check_notice_no = Notice.objects.get(reference_no= notice_refrence_no)
                messages.info(request, 'Notice with this reference no. already exists. ')
                return redirect('create_notice')
            except:
                pass
            

            
            
            new_notice = Notice()
            new_notice.institute = request.user.profile.institute
            new_notice.subject = subject
            new_notice.content = content
            new_notice.publish_date = datetime.date.today()
            new_notice.author = request.user
            new_notice.reference_no= notice_refrence_no
            new_notice.save()
            recipients_valid_list = []

            if 'selected_individual' in request.POST:

                selected_individuals = request.POST.getlist('selected_individual')
                selected_individuals_list = []
                for i in selected_individuals:
                    selected_individuals_list.append(UserProfile.objects.get(pk=i))
                for i in selected_individuals_list:
                    new_notice.recipients_list.add(i)
            else:
                class_student = UserProfile.objects.filter(Class= selected_class, institute= request.user.profile.institute)
                class_parent = AddChild.objects.filter(Class= selected_class, institute= request.user.profile.institute, status='active')
                for st in class_student:
                    recipients_valid_list.append(st)
                for pt in class_parent:
                    recipients_valid_list.append(pt.parent)
                
                for u in recipients_valid_list:
                    user_name = u
                    new_notice.recipients_list.add(user_name)
                return redirect('create_notice')
        context = {
            'user_notices':user_notices,
            'author_classes': author_classes
        }
        return render(request, 'notices/create_notice.html', context)



def creating_new_notice(request):
    if request.method == "POST":
        subject = request.POST.get('notice_subject')
        content = request.POST.get('notice_body')
        selected_class = request.POST.get('notice_class')
        class_student = UserProfile.objects.filter(Class= selected_class, institute= request.user.profile.institute)
        class_parent = AddChild.objects.filter(Class= selected_class, institute= request.user.profile.institute, status='active')
        ad =  request.POST.getlist('audience')
        print(ad)
    
        
        new_notice = Notice()
        new_notice.institute = request.user.profile.institute
        new_notice.subject = subject
        new_notice.content = content
        new_notice.publish_date = datetime.date.today()
        new_notice.author = request.user
        new_notice.save()
        recipients_valid_list = []
        class_student = UserProfile.objects.filter(Class= selected_class, institute= request.user.profile.institute)
        class_parent = AddChild.objects.filter(Class= selected_class, institute= request.user.profile.institute, status='active')
        for st in class_student:
            recipients_valid_list.append(st)
        for pt in class_parent:
            recipients_valid_list.append(pt)
        
        for u in recipients_valid_list:
            user_name = u
            new_notice.recipients_list.add(user_name)
        return HttpResponse('notice published !!!')

        
        

        # all_recipients = Role_Description.objects.filter(institute= request.user.profile.institute)
        # for recipient in all_recipients:
        #     if request.user.user_institute_role.level.level_id <  recipient.level.level_id:
        #         recipients_valid_list.append(recipient)
        
        # for u in recipients_valid_list:
        #     user_name = u.user.profile
        #     new_notice.recipients_list.add(user_name)
        # return HttpResponse('Notice Published Successfully !')
        

        


class Edit_Notice_view(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model= Notice
    fields = ['subject','content']
    template_name = 'notices/update_notice.html'
    success_url ="/notice/create/"

    def test_func(self):
        notice = self.get_object()
        if self.request.user == notice.author:
            return True
        return False


def fetch_deleted_id(request,pk):
    notice_id = request.POST.get('notice_id')
    return HttpResponse(notice_id)

def delete_notice(request):
 
    deleted_notice = Notice.objects.get(pk= request.POST.get('notice_id'))
    try:
        deleted_notice.delete()
        return HttpResponse('True')
    except:
        return HttpResponse('False')


def fetch_notice_audience(request):
    
    selected_class = Classes.objects.get(pk=request.POST.get('class_id') )
    notice_audience=[]
    class_student = UserProfile.objects.filter(Class= selected_class, institute= request.user.profile.institute)
    class_parent = AddChild.objects.filter(Class= selected_class, institute= request.user.profile.institute, status='active')
    

    for st in class_student:
        notice_audience.append(st)
    for pt in class_parent:
        notice_audience.append(pt.parent)
    
    individual_options = ''
    for individual in notice_audience:
        individual_options = individual_options+f"<option value='{individual.id}'>{individual}</option>"
    return HttpResponse(individual_options)
    
    

    
    







            
        
        

    