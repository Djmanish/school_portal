from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from main_app.models import *
from .models import *
from django.views.generic import *
from django.urls import reverse, reverse_lazy
from django.contrib import messages

# Create your views here.

def examschedule(request,pk):
    examschedule_institute=Institute.objects.get(pk=pk)
    examschedule_detail=ExamSchedule.objects.filter(institute=examschedule_institute)

#    Select Exam Class
    if request.method == "POST":
        select_examschedule_class=request.POST.get('selected_class')

        select_examschedule_code=request.POST.get('examschedule_code')
        select_examschedule_type=request.POST.get('examschedule_type')
        examschedule_subject1=request.POST.get('test_subject1')
        examschedule_date1=request.POST.get('test_date1')
        examschedule_time1=request.POST.get('test_time1')
        examschedule_subject_teacher1=request.POST.get('subject_teacher1')
        examschedule_assign_teacher1=request.POST.get('assign_teacher1')
        examschedule_subject2=request.POST.get('test_subject2')
        examschedule_date2=request.POST.get('test_date2')
        examschedule_time2=request.POST.get('test_time2')
        examschedule_subject_teacher2=request.POST.get('subject_teacher2')
        examschedule_assign_teacher2=request.POST.get('assign_teacher2')
        examschedule_subject3=request.POST.get('test_subject3')
        examschedule_date3=request.POST.get('test_date3')
        examschedule_time3=request.POST.get('test_time3')
        examschedule_subject_teacher3=request.POST.get('subject_teacher3')
        examschedule_assign_teacher3=request.POST.get('assign_teacher3')
        examschedule_subject4=request.POST.get('test_subject4')
        examschedule_date4=request.POST.get('test_date4')
        examschedule_time4=request.POST.get('test_time4')
        examschedule_subject_teacher4=request.POST.get('subject_teacher4')
        examschedule_assign_teacher4=request.POST.get('assign_teacher4')
        examschedule_subject5=request.POST.get('test_subject5')
        examschedule_date5=request.POST.get('test_date5')
        examschedule_time5=request.POST.get('test_time5')
        examschedule_subject_teacher5=request.POST.get('subject_teacher5')
        examschedule_assign_teacher5=request.POST.get('assign_teacher5')
        examschedule_subject6=request.POST.get('test_subject6')
        examschedule_date6=request.POST.get('test_date6')
        examschedule_time6=request.POST.get('test_time6')
        examschedule_subject_teacher6=request.POST.get('subject_teacher6')
        examschedule_assign_teacher6=request.POST.get('assign_teacher6')
        examschedule_detail = ExamSchedule.objects.create(institute=request.user.profile.institute, test_code=select_examschedule_code,
         test_type= select_examschedule_type, test_class=select_examschedule_class,
         test_subject1=examschedule_subject1,test_date1=examschedule_date1,test_time1=examschedule_time1,subject_teacher1=examschedule_subject_teacher1,assign_teacher1= examschedule_assign_teacher1,
          test_subject2=examschedule_subject2,test_date2=examschedule_date2,test_time2=examschedule_time2,subject_teacher2=examschedule_subject_teacher2,assign_teacher2= examschedule_assign_teacher2,
           test_subject3=examschedule_subject3,test_date3=examschedule_date3,test_time3=examschedule_time3,subject_teacher3=examschedule_subject_teacher3,assign_teacher3= examschedule_assign_teacher3,
            test_subject4=examschedule_subject4,test_date4=examschedule_date4,test_time4=examschedule_time4,subject_teacher4=examschedule_subject_teacher4,assign_teacher4= examschedule_assign_teacher4,
             test_subject5=examschedule_subject5,test_date5=examschedule_date5,test_time5=examschedule_time5,subject_teacher5=examschedule_subject_teacher5,assign_teacher5= examschedule_assign_teacher5,
              test_subject6=examschedule_subject6,test_date6=examschedule_date6,test_time6=examschedule_time6,subject_teacher6=examschedule_subject_teacher6,assign_teacher6= examschedule_assign_teacher6,)


    all_class = Classes.objects.filter(institute=request.user.profile.institute)
    all_subject=Subjects.objects.filter(institute=request.user.profile.institute)
    teacher_designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='teacher')
    institute_teachers = UserProfile.objects.filter(institute=request.user.profile.institute, designation= teacher_designation_pk )

    context={'all_classes':all_class,
    'examschedule_detail':examschedule_detail,
    'all_subject':all_subject,
    'institute_teachers':institute_teachers,}
    
    return render(request, 'examschedule.html',context)

def update_examschedule(request,pk):
    # institute_examschedule = Institute.objects.get(pk=pk)
    examschedule_update=ExamSchedule.objects.get(pk=pk)
    
    if request.method=="POST":
        select_examschedule_class=request.POST.get('selected_class')
        select_examschedule_code=request.POST.get('examschedule_code')
        select_examschedule_type=request.POST.get('examschedule_type')
        examschedule_subject1=request.POST.get('test_subject1')
        examschedule_date1=request.POST.get('test_date1')
        examschedule_time1=request.POST.get('test_time1')
        examschedule_subject_teacher1=request.POST.get('subject_teacher1')
        examschedule_assign_teacher1=request.POST.get('assign_teacher1')
        examschedule_subject2=request.POST.get('test_subject2')
        examschedule_date2=request.POST.get('test_date2')
        examschedule_time2=request.POST.get('test_time2')
        examschedule_subject_teacher2=request.POST.get('subject_teacher2')
        examschedule_assign_teacher2=request.POST.get('assign_teacher2')
        examschedule_subject3=request.POST.get('test_subject3')
        examschedule_date3=request.POST.get('test_date3')
        examschedule_time3=request.POST.get('test_time3')
        examschedule_subject_teacher3=request.POST.get('subject_teacher3')
        examschedule_assign_teacher3=request.POST.get('assign_teacher3')
        examschedule_subject4=request.POST.get('test_subject4')
        examschedule_date4=request.POST.get('test_date4')
        examschedule_time4=request.POST.get('test_time4')
        examschedule_subject_teacher4=request.POST.get('subject_teacher4')
        examschedule_assign_teacher4=request.POST.get('assign_teacher4')
        examschedule_subject5=request.POST.get('test_subject5')
        examschedule_date5=request.POST.get('test_date5')
        examschedule_time5=request.POST.get('test_time5')
        examschedule_subject_teacher5=request.POST.get('subject_teacher5')
        examschedule_assign_teacher5=request.POST.get('assign_teacher5')
        examschedule_subject6=request.POST.get('test_subject6')
        examschedule_date6=request.POST.get('test_date6')
        examschedule_time6=request.POST.get('test_time6')
        examschedule_subject_teacher6=request.POST.get('subject_teacher6')
        examschedule_assign_teacher6=request.POST.get('assign_teacher6')
        examschedule_update.test_class=select_examschedule_class

        examschedule_update.test_code=select_examschedule_code
        examschedule_update.test_type=select_examschedule_type
        examschedule_update.test_subject1=examschedule_subject1
        examschedule_update.test_date1=examschedule_date1
        examschedule_update.test_time1=examschedule_time1
        examschedule_update.subject_teacher1=examschedule_subject_teacher1
        examschedule_update.assign_teacher1=examschedule_assign_teacher1

        examschedule_update.test_subject2=examschedule_subject2
        examschedule_update.test_date2=examschedule_date2
        examschedule_update.test_time2=examschedule_time2
        examschedule_update.subject_teacher2=examschedule_subject_teacher2
        examschedule_update.assign_teacher2=examschedule_assign_teacher2

        examschedule_update.test_subject3=examschedule_subject3
        examschedule_update.test_date3=examschedule_date3
        examschedule_update.test_time3=examschedule_time3
        examschedule_update.subject_teacher3=examschedule_subject_teacher3
        examschedule_update.assign_teacher3=examschedule_assign_teacher3

        examschedule_update.test_subject4=examschedule_subject4
        examschedule_update.test_date4=examschedule_date4
        examschedule_update.test_time4=examschedule_time4
        examschedule_update.subject_teacher4=examschedule_subject_teacher4
        examschedule_update.assign_teacher4=examschedule_assign_teacher4

        examschedule_update.test_subject5=examschedule_subject5
        examschedule_update.test_date5=examschedule_date5
        examschedule_update.test_time5=examschedule_time5
        examschedule_update.subject_teacher5=examschedule_subject_teacher5
        examschedule_update.assign_teacher5=examschedule_assign_teacher5

        
        examschedule_update.test_subject6=examschedule_subject6
        examschedule_update.test_date6=examschedule_date6
        examschedule_update.test_time6=examschedule_time6
        examschedule_update.subject_teacher6=examschedule_subject_teacher6
        examschedule_update.assign_teacher6=examschedule_assign_teacher6

        examschedule_update.save()
        messages.success(request, 'Exam Schedule Updated Successfully !!!')
        rr=request.user.profile.institute.pk
        return HttpResponseRedirect(f'/examschedule/examschedule/{rr}')
       
    return render(request, 'update_examschedule.html',{'examschedule_update':examschedule_update})