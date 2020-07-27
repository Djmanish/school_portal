from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse

from main_app.models import *
from .models import *
from django.views.generic import *
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from AddChild.models import *
from django.core.exceptions import PermissionDenied
from notices.models import Notice
from django.utils import timezone
import _strptime

# Create your views here.

def create_test_type(request,pk):
            # starting user notice
        if request.user.profile.designation:
                request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
         # ending user notice
        inst = request.user.profile.institute.id

        if pk==inst:        
                edit_exam_date=Edit_Exam_Date.objects.filter(institute=request.user.profile.institute)
                e_start_date=[]

                e_end_date=[]
                for edit_date in edit_exam_date:
                        e_start_date.append(edit_date.edit_start_date)
                        e_end_date.append(edit_date.edit_end_date)
                try:
                        e_start=e_start_date[0]
                except:
                        e_start=None
                try:
                         e_end=e_end_date[0] 
                except:
                        e_end=None  
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
                        messages.success(request, 'New exam type created successfully !')
                        institute_pk = request.user.profile.institute.pk
                        return HttpResponseRedirect(f'/examschedule/examtypelist/{institute_pk}')
                
                context={
                'institute_exam_type':institute_exam_type,
                's_date':e_start,
                'e_date':e_end,
                
                }
                return render(request, 'test_type_list.html', context)
        else:
                        raise PermissionDenied


    
def edit_test_type(request, pk):
            # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
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
          messages.success(request, 'Exam type updated successfully !')
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
        messages.success(request, 'Exam type deleted successfully !')
        institute_pk = request.user.profile.institute.pk
        return HttpResponseRedirect(f'/examschedule/examtypelist/{institute_pk}')


# Edit exam date permission
def edit_exam_date(request,pk):
        institute_pk = request.user.profile.institute.pk
        edit_exam_date=Edit_Exam_Date.objects.filter(institute=request.user.profile.institute)
        inst_id = request.user.profile.institute.pk
       
        if request.method=="POST":
               
              
                start_date=str(request.POST.get('start_date'))

                end_date= str(request.POST.get('end_date'))
                schedule_date= datetime.datetime.strptime(start_date, '%Y-%m-%d')

                
                        
                if schedule_date<datetime.datetime.now():
                                        messages.error(request, 'Date must be in future!')
                                        return redirect(f'/examschedule/examtypelist/{inst_id}') 
                edit_institute=request.user.profile.institute.id
                edit_exam_institute=Institute.objects.get(pk=edit_institute)
                
                edit_data=Edit_Exam_Date()
                
                edit_data.institute=edit_exam_institute
                edit_data.edit_start_date=start_date
                edit_data.edit_end_date=end_date
                edit_data.save()

        
                messages.success(request, 'Edit date stored successfully!')
                return HttpResponseRedirect(f'/examschedule/examtypelist/{institute_pk}')
        context={
                       'edit_exam_date':edit_exam_date,
                       
                       
                        
        }
        return render(request, 'test_type_list.html', context)





# function for create exam type
def exam_schedule(request,pk):
        # starting user notice
        if request.user.profile.designation:
                request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
        # ending user notice
        inst = request.user.profile.institute.id

        # if id does not match with institute id
        if pk!=inst:
                raise PermissionDenied 
        # fetch the institute id
        institute_exam_schedule_data = Institute.objects.get(pk=pk)
        institute_exam_schedule = ExamDetails.objects.filter(institute=institute_exam_schedule_data)

        # fetch the teachers of current institute
        designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='teacher')
        institute_teachers = UserProfile.objects.filter(institute= request.user.profile.institute, designation=designation_pk)

        #  fetch the value of selected class from the dropdown menu
        exam_class = Classes.objects.filter(institute=request.user.profile.institute)
        exam_type_schedule= ExamType.objects.filter(institute=request.user.profile.institute)
        institute_pk = request.user.profile.institute.pk

        if request.method=="POST":
                # get the value from the upper selected box
                select_class_for_schedule = request.POST.get('selected_class') #selected class
                selected_class = Classes.objects.get(pk=select_class_for_schedule)

                select_exam_for_schedule = request.POST.get('selected_exam_type')#selected exam type
                selected_exam_type = ExamType.objects.get(pk=select_exam_for_schedule)
                
                
                exam_class_subject=Subjects.objects.filter(subject_class=selected_class)#exam class

                # get the value of sr no
                sr_no=ExamDetails.objects.filter(exam_type__exam_type=selected_exam_type,exam_class=selected_class).values('exam_sr_no').distinct().count()+1
                
                # check exam type limit
                exam_type_limit=ExamType.objects.filter(institute=request.user.profile.institute, exam_type=selected_exam_type)
                for exam_limit in exam_type_limit:
                        limit=exam_limit.exam_max_limit
                        limit_exam=int(limit)
                
                if sr_no<=limit_exam:
                    pass
                else:
                    messages.error(request, 'Exam Limit has exceeded!')
                    return HttpResponseRedirect(f'/examschedule/examschedule/{institute_pk}')

                if exam_class_subject:

                        context={
                        'exam_class':exam_class,
                        'institute_teachers':institute_teachers,
                        'exam_type_schedule':exam_type_schedule,
                        'exam_class_subject':exam_class_subject,
                        'selected_class':selected_class,
                        'selected_exam_type':selected_exam_type,
                        'sr_no':sr_no,
                        'institute_exam_schedule_data':institute_exam_schedule_data,

                        
                        }
                        return render(request,'examschedule.html',context)
                else:
                        messages.error(request, 'No subjects found for selected class!')
                        return HttpResponseRedirect(f'/examschedule/examschedule/{institute_pk}')

        context={
                'exam_class':exam_class,
                'institute_teachers':institute_teachers,
                'exam_type_schedule':exam_type_schedule,
                
                
                }
        return render(request,'examschedule.html',context)

def create_exam_schedule(request, pk):
        # starting user notice
        if request.user.profile.designation:
                 request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
        # ending user notice
        
        # get the institute id
        institute_exam_schedule_data = Institute.objects.get(pk=pk)
        institute_exam_schedule = ExamDetails.objects.filter(institute=institute_exam_schedule_data)
        inst_id=request.user.profile.institute.id

        # get all the teachers
        designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='teacher')
        institute_teachers = UserProfile.objects.filter(institute= request.user.profile.institute, designation=designation_pk )

        # today's time
        today_date=timezone.now()

        if request.method == "POST":
                selected_class=Classes.objects.get(pk=request.POST.get('selected_class_hidden'))
                select_exam_type= ExamType.objects.get(pk=request.POST.get('exam_type_id_hidden'))
                exam_code=request.POST.get('exam_institute_code')
                exam_sr_no = request.POST.get('sr_no')
                sr_no=ExamDetails.objects.filter(exam_type__exam_type=select_exam_type,exam_class=selected_class).values('exam_sr_no').distinct().count()+1
               
                for subject,subject_teacher,date,start_time,end_time,assign_teacher in zip(request.POST.getlist('select_exam_subject'), request.POST.getlist('select_exam_subject_teacher'),request.POST.getlist('select_date'),request.POST.getlist('select_start_time'),request.POST.getlist('select_end_time'),request.POST.getlist('assign_teacher')):
                       
                        schedule_date= datetime.datetime.strptime(date, '%Y-%m-%d')
                        
                        if schedule_date<datetime.datetime.now():
                                messages.error(request, 'Date must be in future!')
                                return redirect(f'/examschedule/examschedule/{inst_id}')  
                        
                        else: 
                                pass
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
                        new_exam.exam_type=select_exam_type
                        new_exam.save()
        messages.success(request, 'New exam schedule created successfully!')
                        
         
        return redirect(f'/examschedule/examschedule/{inst_id}') 


def examschedule_view(request,pk):
        # starting user notice
        if request.user.profile.designation:
                request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
        # ending user notice
        inst = request.user.profile.institute.id

        if pk==inst:
            institute_exam_schedule = ExamDetails.objects.filter(institute=request.user.profile.institute)
            institute_exam_type=ExamType.objects.filter(institute=request.user.profile.institute)
            exam_class = Classes.objects.filter(institute=request.user.profile.institute)
            institute_pk = request.user.profile.institute.pk
            user_children= AddChild.objects.filter(parent= request.user.profile, status="active")
            parent_student_list = []
            for st in user_children:
                        student= UserProfile.objects.get(pk=st.child.id)
                        parent_student_list.append(student)

            if request.method=="POST":
                select_exam_type = request.POST.get('selected_exam_type')
                if select_exam_type==None:
                    etype=ExamType.objects.get(institute= request.user.profile.institute, exam_type=select_exam_type)
                    exam_type=etype.id
                    select_exam_type=exam_type
                exam_type_data = ExamType.objects.get(pk=select_exam_type)
                select_exam_type_no = request.POST.get('selected_exam_type_no')
                if request.user.profile.designation.level_name=='student':
                        selected_class = request.user.profile.Class
                        
                        exam_details = ExamDetails.objects.filter(institute=request.user.profile.institute, exam_type__exam_type= exam_type_data,exam_sr_no= select_exam_type_no,exam_class__name=selected_class)
                        if exam_details:
                                context = {
                                'selected_class':selected_class,
                                'exam_type_data':exam_type_data,
                                'select_exam_type_no':select_exam_type_no,
                                'parent_student_list':parent_student_list,
                                'exam_details': exam_details,
                                'institute_exam_schedule':institute_exam_schedule,
                                'institute_exam_type':institute_exam_type,
                                }
                        
                                return render(request,'update_examschedule.html', context)
                        else:
                                messages.error(request, 'No result found for this selection!')
                                return redirect(f'/examschedule/examschedule/{inst}')
                        
                        
                else:
                        if request.user.profile.designation.level_name=='parent':
                                select_st=request.POST.get('selected_student')
                                
                                selected_student=User.objects.get(pk=select_st)
                                student_institute=selected_student.profile.institute
                                institute_exam_type=ExamType.objects.filter(institute=student_institute)
                                
                                student_class= selected_student.profile.Class

                                exam_details = ExamDetails.objects.filter(institute=request.user.profile.institute, exam_type__exam_type= exam_type_data,exam_sr_no= select_exam_type_no,exam_class__name=student_class)
                                
                                context = {
                                        
                                        'exam_class':exam_class,
                                        'parent_student_list':parent_student_list,
                                        'exam_type_data':exam_type_data,
                                        'select_exam_type_no':select_exam_type_no,      
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
                                exam_details = ExamDetails.objects.filter(institute=request.user.profile.institute, exam_type__exam_type= exam_type_data,exam_sr_no= select_exam_type_no,exam_class__name=selected_class )
                                if exam_details:
                                
                                        context = {
                                        'select_class_for_schedule':select_class_for_schedule,
                                        'exam_class':exam_class,
                                        'selected_class':selected_class,
                                        'exam_type_data':exam_type_data,
                                        'select_exam_type_no':select_exam_type_no,      
                                        'exam_details': exam_details,
                                        'institute_exam_schedule':institute_exam_schedule,
                                        'institute_exam_type':institute_exam_type,
                                        }
                                
                                        return render(request,'update_examschedule.html', context)
                                else:
                                        messages.info(request, 'There is no exam data for this selection !')
                        
                                        return HttpResponseRedirect(f'/examschedule/examschedule/view/{institute_pk}')
            context={
              'exam_class':exam_class,
              'institute_exam_schedule':institute_exam_schedule,
              'institute_exam_type':institute_exam_type,
              'parent_student_list':parent_student_list,
              
             
                     }
            return render(request,'update_examschedule.html', context)
        else:
                raise PermissionDenied

def edit_examschedule(request,pk):
    # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
    examdetails_info= ExamDetails.objects.get(pk=pk)
    designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='teacher')
    institute_teachers = UserProfile.objects.filter(institute= request.user.profile.institute, designation=designation_pk )

    if request.method=="POST":
          select_exam_subject=request.POST.get('select_exam_subject')
          select_exam_subject_teacher= request.POST.get('select_exam_subject_teacher')
          selected_subject_teacher=User.objects.get(pk=select_exam_subject_teacher)
          
          select_date = request.POST.get('select_date')
          select_start_time = request.POST.get('select_start_time')
          
          select_end_time = request.POST.get('select_end_time')
          assign_teacher = request.POST.get('assign_teacher')
          selected_assign_teacher=User.objects.get(pk=assign_teacher)
     
          examdetails_info.institute=request.user.profile.institute
          examdetails_info.exam_subject=select_exam_subject
          examdetails_info.exam_subject_teacher=selected_subject_teacher
          examdetails_info.exam_date=select_date
          examdetails_info.exam_start_time=select_start_time
          

          examdetails_info.exam_end_time=select_end_time

          examdetails_info.exam_assign_teacher=selected_assign_teacher


         
          examdetails_info.save()
          messages.success(request, 'Exam schedule updated successfully !')
          institute_pk = request.user.profile.institute.pk
          return HttpResponseRedirect(f'/examschedule/examschedule/view/{institute_pk}')
    
    context={
      # 'institute_exam_type':institute_exam_type,
      'examdetails_info':examdetails_info,
      'institute_teachers':institute_teachers,
      
            }
    return render(request, 'edit_exam_schedule.html', context)

def delete_examschedule(request, pk):
        # starting user notice
        if request.user.profile.designation:
                request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
        # ending user notice
        examdetails_info= ExamDetails.objects.get(pk=pk)
      
        examdetails_info.exam_subject="null"
        examdetails_info.exam_subject_teacher="null"
        examdetails_info.exam_start_time="null"
        examdetails_info.exam_end_time="null"
        
        examdetails_info.delete()
        messages.success(request, 'Exam schedule deleted successfully !')
        institute_pk = request.user.profile.institute.pk
        return HttpResponseRedirect(f'/examschedule/examschedule/view/{institute_pk}')


def fetch_max_sr_no(request):
  exam_type_id = request.POST.get('exam_type_id')
  exam_type=ExamType.objects.get(pk=exam_type_id)
  
  max_exam_sr_no = ExamDetails.objects.filter(exam_type=exam_type_id).values('exam_sr_no').distinct()
 
  individual_sr_no = "<option>--Exam Type No.--</option>"
  for sr_no in max_exam_sr_no:
    individual_sr_no = individual_sr_no + f"<option>"+sr_no['exam_sr_no']+"</option>" 
     
  return HttpResponse(individual_sr_no)


  
def fetch_no(request):
  exam_type_id = request.POST.get('exam_type_no')
  exam_type=ExamType.objects.get(pk=exam_type_id)
  
  max_exam_sr_no = ExamDetails.objects.filter(exam_type=exam_type_id).values('exam_sr_no').distinct()
 
  individual_sr_no = "<option>--Exam Type No.--</option>"
  for sr_no in max_exam_sr_no:
    individual_sr_no = individual_sr_no + f"<option>"+sr_no['exam_sr_no']+"</option>" 
     
  return HttpResponse(individual_sr_no)

def selected_exam_type(request):
        select_st= request.POST.get('selected_student')
        selected_student=UserProfile.objects.get(pk=select_st)
        student_institute=selected_student.institute
        institute_exam_type=ExamType.objects.filter(institute=student_institute)
        # student_exam_type = ExamDetails.objects.filter(institute=institute_exam_type).values('exam_type').distinct()
        
        
        individual_exam_type = "<option>--Exam Type--</option>"
        for etype in institute_exam_type:
                individual_exam_type = individual_exam_type + f"<option value={etype.id}>{etype}</option>" 
        
        return HttpResponse(individual_exam_type)
    