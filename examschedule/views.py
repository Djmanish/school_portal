from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from main_app.models import *
from .models import *
from django.views.generic import *
from django.urls import reverse, reverse_lazy
from django.contrib import messages

# Create your views here.

def create_test_type(request,pk):
  if request.method=="POST":
    exam_type_name=request.POST.get()
  return render(request, 'test_type_list.html')

def exam_schedule(request,pk):
        # fetch the institute and Exam Details based on the institute
            institute_exam_schedule_data = Institute.objects.get(pk=pk)
            institute_exam_schedule = ExamDetails.objects.filter(institute=institute_exam_schedule_data)
    
      # fetch the teachers of current institute
            designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='teacher')
            institute_teachers = UserProfile.objects.filter(institute= request.user.profile.institute, designation=designation_pk )

      
        #  fetch the value of selected class from the dropdown menu
            exam_class = Classes.objects.filter(institute=request.user.profile.institute)
            select_class_for_schedule = request.GET.get('selected_class')
            if select_class_for_schedule == None:
                    first_class = Classes.objects.filter(institute= request.user.profile.institute).last()
                    first_class_id = first_class.id
                    select_class_for_schedule= first_class_id
            selected_class = Classes.objects.get(pk=select_class_for_schedule)
            
            
            
        # fetching the value of exam from the given drop down
            exam_type_schedule= ExamType.objects.all()
            
            select_exam_for_schedule = request.GET.get('selected_exam_type')
            if select_exam_for_schedule==None:
                   etype=ExamType.objects.all().last()
                   exam_type_id=etype.id
                   select_exam_for_schedule=exam_type_id
            exam_type_id=ExamType.objects.get(pk=select_exam_for_schedule)
                
        
          #  to fetch the value of Subject and Subject Teacher
            exam_class_subject=Subjects.objects.filter(subject_class=selected_class)
          
          # Count the number if tyoe the exam type selected 
            sr_no=ExamDetails.objects.filter(institute=request.user.profile.institute, exam_class=selected_class, exam_type=exam_type_id).count()
            
       
            if request.method=="POST":
              for i in request.POST.getlist('select_exam_subject'):
                print(i)
              
              for subject,subject_teacher,date,start_time,end_time,assign_teacher,exam_code in zip(request.POST.getlist('select_exam_subject'), request.POST.getlist('select_exam_subject_teacher'),request.POST.getlist('select_date'),request.POST.getlist('select_start_time'),request.POST.getlist('select_end_time'),request.POST.getlist('assign_teacher'),request.POST.getlist('exam_institute_code')):
                selected_class=Classes.objects.get(pk=request.GET.get('selected_class'))
                select_exam_type= ExamType.objects.get(pk=request.GET.get('selected_exam_type'))
                new_exam = ExamDetails()
                new_exam.institute=request.user.profile.institute 
                new_exam.exam_subject = Subjects.objects.get(pk=subject)
                new_exam.exam_subject_teacher =User.objects.get(pk=subject_teacher)
                new_exam.exam_date=date
                new_exam.exam_start_time=start_time
                new_exam.exam_end_time=end_time
                new_exam.exam_sr_no=sr_no
                new_exam.exam_code=exam_code
                new_exam.exam_assign_teacher=User.objects.get(pk=assign_teacher)
                new_exam.exam_class=selected_class
                new_exam.exam_type=exam_type_id
                new_exam.save()
                messages.success(request, 'New Exam Schedule Created successfully !!!')

          
                
            context={
                 'institute_exam_schedule_data':institute_exam_schedule_data,  
                 'exam_class':exam_class,
                 'exam_class_subject':exam_class_subject,
                 'institute_teachers':institute_teachers,
                 'exam_type_schedule':exam_type_schedule,
                 'selected_class':selected_class,
                 'sr_no':sr_no,
                 'institute_exam_schedule':institute_exam_schedule,
                 'exam_type_id':exam_type_id,

                
                                   
                    }
       
            return render(request,'examschedule.html',context)


 

def examschedule_view(request,pk):
            institute_exam_schedule = Institute.objects.get(pk=pk)
            institute_exam_schedule = ExamDetails.objects.filter(institute=institute_exam_schedule)

      
            context={
             
              
              'institute_exam_schedule':institute_exam_schedule


            }
            return render(request,'update_examschedule.html', context)
