from django.shortcuts import render, redirect
from django.utils import timezone
from .models import *
import datetime
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from AddChild.models import *
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.

def all_notices(request):  
    # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
    user_notices = Notice.objects.filter(institute=request.user.profile.institute, recipients_list = request.user.profile, publish_date__lte=timezone.now()).order_by('-id')

    page = request.GET.get('page', 1)
    paginator = Paginator(user_notices, 30)
    try:
        user_notices = paginator.page(page)
    except PageNotAnInteger:
        user_notices = paginator.page(1)
    except EmptyPage:
        user_notices = paginator.page(paginator.num_pages)

    context ={
        'all_notices': user_notices,        
    }
    return render(request, 'notices/all_notices_list.html', context)



def create_notice(request):
    # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
    if request.user.user_institute_role.level.level_name == 'student' or request.user.user_institute_role.level.level_name == 'parent':
        messages.info(request, 'You may not have permission to create a notice !')
        return redirect('not_found')
    else:
        user_notices = Notice.objects.filter(author= request.user).order_by('-id')
        author_classes= [] # showing classes according to user
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
            publish_datetime =datetime.datetime.strptime(request.POST.get('pubdatetime'), '%Y-%m-%dT%H:%M')
            notice_refrence_no = request.POST.get('notice_refrence_no').strip()

            if not notice_refrence_no=="":
                try:
                    check_notice_no = Notice.objects.get(reference_no= notice_refrence_no)
                    messages.error(request, 'Notice with this reference no. already exists ! ')
                    return redirect('create_notice')
                except:
                    pass
                
            new_notice = Notice()
            new_notice.institute = request.user.profile.institute
            new_notice.subject = subject
            new_notice.content = content
            # new_notice.publish_date = timezone.now()
            new_notice.author = request.user
            new_notice.created_at = timezone.now()
            new_notice.publish_date = publish_datetime
            new_notice.reference_no= notice_refrence_no
            try:
                new_notice.save()
                messages.success(request, "Notice created successfully !")
            except:
                messages.error(request, 'Could not Create notice, Try again !')
                return redirect('create_notice')

            recipients_valid_list = []

            if 'selected_individual' in request.POST:
                selected_individuals = request.POST.getlist('selected_individual')
                selected_individuals_list = []
                for i in selected_individuals: #test this
                    selected_individuals_list.append(UserProfile.objects.get(pk=i))
                for i in selected_individuals_list:
                    new_notice.recipients_list.add(i)
                new_notice.recipients_list.add(request.user.profile)
            elif 'all_classes_check' in request.POST:
                all_students = UserProfile.objects.filter(designation__level_name='student', institute= request.user.profile.institute)
                all_parents = UserProfile.objects.filter(designation__level_name='parent', institute= request.user.profile.institute )
                for st in all_students:
                    recipients_valid_list.append(st)
                for pt in all_parents:
                    recipients_valid_list.append(pt)
                
                for i in recipients_valid_list:
                    new_notice.recipients_list.add(i)
                new_notice.recipients_list.add(request.user.profile)
                return redirect('create_notice')

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
                new_notice.recipients_list.add(request.user.profile)
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
        

        
from .forms import NoticeUpdateForm

class Edit_Notice_view(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model= Notice
    # fields = ['subject','content']
    template_name = 'notices/update_notice.html'
    success_url ="/notice/create/"
    form_class = NoticeUpdateForm
    success_message = "Notice updated successfully !"

    def form_valid(self, form):
        print()
        
        form.instance.publish_date = datetime.datetime.strptime(self.request.POST['pubdatetime'], '%Y-%m-%dT%H:%M') 
        return super().form_valid(form)

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

    class_assigned_teacher = Subjects.objects.filter(subject_class=selected_class )
    

    for st in class_student:
        notice_audience.append(st)
    for pt in class_parent:
        if pt.parent in notice_audience:
            pass
        else:
            notice_audience.append(pt.parent)
    for teacher in class_assigned_teacher:
        if teacher.subject_teacher.profile in notice_audience:
            pass
        else:
            notice_audience.append(teacher.subject_teacher.profile)
    
    individual_options = ''
    for individual in notice_audience:
        individual_options = individual_options+f"<option value='{individual.id}'>{individual.first_name} {individual.last_name}  ({individual.designation})</option>"
    
    
    return HttpResponse(individual_options)
    
    

    
    







            
        
        

    