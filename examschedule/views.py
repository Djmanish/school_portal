from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from main_app.models import *
from .models import *
from django.views.generic import *
from django.urls import reverse, reverse_lazy
from django.contrib import messages

# Create your views here.

def exam_schedule(request,pk):
            designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='teacher')
            institute_teachers = UserProfile.objects.filter(institute= request.user.profile.institute, designation=designation_pk )
            select_class_for_schedule = request.GET.get('selected_class') # class selected to view
            if select_class_for_schedule == None:
                    first_class = Classes.objects.filter(institute= request.user.profile.institute).last()
                    first_class_id = first_class.id
                    select_class_for_schedule= first_class_id
            selected_class = Classes.objects.get(pk=select_class_for_schedule)
            #fetching the class instance seleted to view
            exam_class = Classes.objects.filter(institute=request.user.profile.institute)
            exam_class_subject=Subjects.objects.filter(subject_class=selected_class)
         
            if request.method=="POST":
         
                selected_class=Classes.objects.get(pk=request.GET.get('selected_class'))
                exam_subject=Subjects.objects.get(pk=request.POST.get('select_exam_subject'))
                exam_subject_teacher=User.objects.get(pk=request.POST.get('select_exam_subject_teacher'))
                select_date=request.POST.get('select_date')
                select_start_time=request.POST.get('select_start_time')
                select_end_time=request.POST.get('select_end_time')
                assign_teacher=User.objects.get(pk=request.POST.get('assign_teacher'))
               
                new_exam_schedule = ExamDetails.objects.create(institute=request.user.profile.institute,
                    exam_class=selected_class,
                    exam_subject=exam_subject,
                    exam_subject_teacher=exam_subject_teacher,
                    exam_date=select_date,
                    exam_start_time= select_start_time, 
                    exam_end_time= select_end_time,
                    exam_assign_teacher=assign_teacher)
                messages.success(request, 'New ExamSchedule Created successfully !!!')
 
            context={
                 'exam_class':exam_class,
                 'exam_class_subject':exam_class_subject,
                 'institute_teachers':institute_teachers,
                                   
                                    }
                                    
            
    
            return render(request,'examschedule.html',context)


   