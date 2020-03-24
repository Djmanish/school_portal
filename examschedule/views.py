from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse

from main_app.models import *
from .models import *
from django.views.generic import *
from django.urls import reverse, reverse_lazy
from django.contrib import messages


# Create your views here.

def create_test_type(request,pk):
    
    institute_exam_type=ExamType.objects.filter(institute=request.user.profile.institute)
    exam_sr_no=ExamType.objects.filter(institute=request.user.profile.institute).count()+1
   
    if request.method=="POST":
          exam_type_name=request.POST.get('exam_type')
          exam_max_marks= request.POST.get('exam_max_marks')
          exam_max_limit = request.POST.get('exam_max_limit')
          exam_per_final_score = request.POST.get('exam_per_final_score')
          examtype= ExamType()
          examtype.institute=request.user.profile.institute
          examtype.exam_type=exam_type_name
          examtype.exam_max_marks=exam_max_marks
          examtype.exam_max_limit=exam_max_limit
          examtype.exam_per_final_score=exam_per_final_score
          examtype.exam_type_sr_no=exam_sr_no
          examtype.save()
          messages.success(request, 'New Exam Type Created successfully !!!')
          institute_pk = request.user.profile.institute.pk
          return HttpResponseRedirect(f'/examschedule/examtypelist/{institute_pk}')
    
    context={
      'institute_exam_type':institute_exam_type,
      
    }
    return render(request, 'test_type_list.html', context)

    
def edit_test_type(request, pk):
    test_type_info= ExamType.objects.get(pk=pk)
    # institute_exam_type=ExamType.objects.filter(institute=request.user.profile.institute)
    

    if request.method=="POST":
          exam_type_name=request.POST.get('exam_type')
          exam_max_marks= request.POST.get('exam_max_marks')
          exam_max_limit = request.POST.get('exam_max_limit')
          exam_per_final_score = request.POST.get('exam_per_final_score')
          
          test_type_info.institute=request.user.profile.institute
          test_type_info.exam_type=exam_type_name
          test_type_info.exam_max_marks=exam_max_marks
          test_type_info.exam_max_limit=exam_max_limit
          test_type_info.exam_per_final_score=exam_per_final_score
          # examtype.exam_type_sr_no=exam_sr_no
          test_type_info.save()
          messages.success(request, 'Exam Type Updated Successfully !!!')
          institute_pk = request.user.profile.institute.pk
          return HttpResponseRedirect(f'/examschedule/examtypelist/{institute_pk}')
    
    context={
      # 'institute_exam_type':institute_exam_type,
      'test_type_info':test_type_info,
      
            }
    return render(request, 'edit_exam_type.html', context)

def delete_test_type(request, pk):
        test_type_info= ExamType.objects.get(pk=pk)
      
        test_type_info.exam_max_marks="null"
        test_type_info.exam_max_limit="null"
        test_type_info.exam_per_final_score="null"
        
        test_type_info.delete()
        messages.success(request, 'Exam Type Deleted Successfully !!!')
        institute_pk = request.user.profile.institute.pk
        return HttpResponseRedirect(f'/examschedule/examtypelist/{institute_pk}')


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
            
            exam_type_schedule= ExamType.objects.filter(institute=request.user.profile.institute)
            if exam_type_schedule:
                     pass
            else:
                    messages.info(request, 'It seems there are no exam types in the institute. First create the exam type then you can create Exam Cchedule')
                    return redirect('not_found')
                    
            
            select_exam_for_schedule = request.GET.get('selected_exam_type')
         
            if select_exam_for_schedule==None:
                   etype=ExamType.objects.filter(institute= request.user.profile.institute).first()
                   exam_type=etype.id
                   select_exam_for_schedule=exam_type
            exam_type_id=ExamType.objects.get(pk=select_exam_for_schedule)
            
              #  to fetch the length of exam limit from exam type
            exam_type_limit=ExamType.objects.filter(institute=request.user.profile.institute, exam_type=exam_type_id)
            for exam_limit in exam_type_limit:
                limit=exam_limit.exam_max_limit
                limit_exam=int(limit)

          #  to fetch the value of Subject and Subject Teacher
            exam_class_subject=Subjects.objects.filter(subject_class=selected_class)

           
          
          # Count the number if type the exam type selected
           
            sr_no=ExamDetails.objects.filter(exam_type__exam_type=exam_type_id,exam_class=selected_class).values('exam_sr_no').distinct().count()+1
           
            if sr_no<=limit_exam:
                    pass
            else:
                    messages.info(request, 'Exam Limit has exceeded')
                    return redirect('not_found')

           
            if request.method == "POST":
              for subject,subject_teacher,date,start_time,end_time,assign_teacher in zip(request.POST.getlist('select_exam_subject'), request.POST.getlist('select_exam_subject_teacher'),request.POST.getlist('select_date'),request.POST.getlist('select_start_time'),request.POST.getlist('select_end_time'),request.POST.getlist('assign_teacher')):
                  
                  
                  selected_class=Classes.objects.get(pk=request.GET.get('selected_class'))
                  select_exam_type= ExamType.objects.get(pk=request.GET.get('selected_exam_type'))
                  exam_code=request.POST.get('exam_institute_code')
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
            institute_exam_schedule = ExamDetails.objects.filter(institute=request.user.profile.institute)
            institute_exam_type=ExamType.objects.filter(institute=request.user.profile.institute)
            exam_class = Classes.objects.filter(institute=request.user.profile.institute)

            if request.method=="POST":
                select_exam_type = request.POST.get('selected_exam_type')
                select_exam_type_no = request.POST.get('selected_exam_type_no')
                if request.user.profile.designation.level_name=='student':
                        selected_class = request.user.profile.Class
                        exam_details = ExamDetails.objects.filter(institute=request.user.profile.institute, exam_type__exam_type= select_exam_type,exam_sr_no= select_exam_type_no,exam_class__name=selected_class )
                        context = {
                        
                        'exam_details': exam_details,
                        'institute_exam_schedule':institute_exam_schedule,
                        'institute_exam_type':institute_exam_type,
                        }
                
                        return render(request,'update_examschedule.html', context)
                        
                else:
                        select_class_for_schedule = request.POST.get('selected_class')
                        if select_class_for_schedule == None:
                                first_class = Classes.objects.filter(institute= request.user.profile.institute).last()
                                first_class_id = first_class.id
                                select_class_for_schedule= first_class_id
                        selected_class = Classes.objects.get(pk=select_class_for_schedule)
                        exam_details = ExamDetails.objects.filter(institute=request.user.profile.institute, exam_type__exam_type= select_exam_type,exam_sr_no= select_exam_type_no,exam_class__name=selected_class )
                
                
                        context = {
                        'exam_class':exam_class,
                        'exam_details': exam_details,
                        'institute_exam_schedule':institute_exam_schedule,
                        'institute_exam_type':institute_exam_type,
                        }
                
                        return render(request,'update_examschedule.html', context)
            
            context={
              'exam_class':exam_class,
              'institute_exam_schedule':institute_exam_schedule,
              'institute_exam_type':institute_exam_type,
             
                     }
            return render(request,'update_examschedule.html', context)

def edit_examschedule(request,pk):
    examdetails_info= ExamDetails.objects.get(pk=pk)
    designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='teacher')
    institute_teachers = UserProfile.objects.filter(institute= request.user.profile.institute, designation=designation_pk )

    if request.method=="POST":
          select_exam_subject=request.POST.get('select_exam_subject')
          select_exam_subject_teacher= request.POST.get('select_exam_subject_teacher')
          select_date = request.POST.get('select_date')
          select_start_time = request.POST.get('select_start_time')
          select_end_time = request.POST.get('select_end_time')
          assign_teacher = request.POST.get('assign_teacher')
     
          examdetails_info.institute=request.user.profile.institute
          examdetails_info.exam_subject=select_exam_subject
          examdetails_info.exam_subject_teacher=select_exam_subject_teacher
          examdetails_info.exam_date=select_date
          examdetails_info.exam_start_time=select_start_time

          examdetails_info.exam_end_time=select_end_time

          # examdetails_info.exam_assign_teacher=assign_teacher


         
          examdetails_info.save()
          messages.success(request, 'Exam Schedule Updated Successfully !!!')
          institute_pk = request.user.profile.institute.pk
          return HttpResponseRedirect(f'/examschedule/examschedule/view/{institute_pk}')
    
    context={
      # 'institute_exam_type':institute_exam_type,
      'examdetails_info':examdetails_info,
      'institute_teachers':institute_teachers,
      
            }
    return render(request, 'edit_exam_schedule.html', context)

def delete_examschedule(request, pk):
        examdetails_info= ExamDetails.objects.get(pk=pk)
      
        examdetails_info.exam_subject="null"
        examdetails_info.exam_subject_teacher="null"
        examdetails_info.exam_start_time="null"
        examdetails_info.exam_end_time="null"
        
        examdetails_info.delete()
        messages.success(request, 'Exam Schedule Deleted Successfully !!!')
        institute_pk = request.user.profile.institute.pk
        return HttpResponseRedirect(f'/examschedule/examschedule/view/{institute_pk}')


def fetch_max_sr_no(request):
  exam_type_id = request.POST.get('exam_type_id')
  
  max_exam_sr_no = ExamDetails.objects.filter(exam_type__exam_type=exam_type_id).values('exam_sr_no').distinct()
 
  individual_sr_no = "<option>--Exam Type No.--</option>"
  for sr_no in max_exam_sr_no:
    individual_sr_no = individual_sr_no + f"<option>"+sr_no['exam_sr_no']+"</option>" 
     
  return HttpResponse(individual_sr_no)
    