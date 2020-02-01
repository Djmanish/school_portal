from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from main_app.models import *
from .models import *
from django.views.generic import *
from django.urls import reverse, reverse_lazy
from django.contrib import messages

# Create your views here.
# class MemberList(ListView):
#     model=ExamDetails

def exam_schedule(request,pk):
            institute_exam_schedule = Institute.objects.get(pk=pk)
            institute_exam_schedule = ExamDetails.objects.filter(institute=institute_exam_schedule)
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
              for i,j,k,l,m,n in zip(request.POST.getlist('select_exam_subject'),request.POST.getlist('select_exam_subject_teacher'),request.POST.getlist('select_date'), request.POST.getlist('select_start_time'), request.POST.getlist('select_end_time'),request.POST.getlist('assign_teacher')):
                  
                selected_class=Classes.objects.get(pk=request.GET.get('selected_class'))

                exam_subjects_list = request.POST.getlist('select_exam_subject')
                
                exam_subject_teacher_list=request.POST.getlist('select_exam_subject_teacher')
                select_date=request.POST.getlist('select_date')
                select_start_time=request.POST.getlist('select_start_time')
                select_end_time=request.POST.getlist('select_end_time')
                assign_teacher=request.POST.getlist('assign_teacher')
                
                for i in exam_subjects_list  :
                 new_exam = ExamDetails() 
                 new_exam.exam_subject = Subjects.objects.get(pk=i )
                    
                 new_exam.exam_subject_teacher =User.objects.get(pk=j)
                 new_exam.exam_date=k
                 new_exam.exam_start_time=l
                 new_exam.exam_end_time=m

                 new_exam.exam_assign_teacher=User.objects.get(pk=n)
                 new_exam.institute=request.user.profile.institute
                 new_exam.exam_class=selected_class
                 new_exam.save()
                messages.success(request, 'New Exam Schedule Created successfully !!!')

          
                
            context={
                 'exam_class':exam_class,
                 'exam_class_subject':exam_class_subject,
                 'institute_teachers':institute_teachers,
                                   
                                    }
       
            return render(request,'examschedule.html',context)


def exam_type(request,pk):
      
      if request.method=="POST":
          select_class_for_schedule = request.GET.get('selected_class') # class selected to view
          exam_type=request.POST['test_type']
          new_exam_type=ExamType.objects.create(institute = request.user.profile.institute,exam_type=exam_type)
          institute_id=request.user.profile.institute.id
          return HttpResponseRedirect(f'/examschedule/examtypelist/{institute_id}')
          

def create_test_type(request,pk):
         institute_create_test_type = Institute.objects.get(pk=pk)
         institute_exam_test_type = ExamType.objects.filter(institute=institute_create_test_type)
         context={
           'institute_exam_test_type':institute_exam_test_type 

         }

         return render(request,'test_type_list.html')
