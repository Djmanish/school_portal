from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, Http404
from .models import *
from main_app.models import *
from examschedule.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.db.models import Count
import datetime
import statistics 
from django.core.cache import cache 
import random   
from AddChild.models import * 
from django.core.exceptions import PermissionDenied
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.contrib.sessions.models import Session
from django.utils import timezone
from notices.models import *
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile
# Create your views here.
def exam_result(request,pk):
  inst = request.user.profile.institute.id
  if pk==inst:
        # starting user notice
      if request.user.profile.designation:
                request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
        # ending user notice
    
      result_institute=Institute.objects.get(pk=pk)
      exam_result_institute=ExamResult.objects.filter(institute=result_institute)
      #  to fetch the logged in  subject teacher
      subject_result=Subjects.objects.filter(institute=request.user.profile.institute, subject_teacher=request.user)
      institute_exam_type=ExamType.objects.filter(institute=request.user.profile.institute)
    # -----------------------------------------------------------------------------------
      if request.method=="POST":
        selected_subject = Subjects.objects.get(pk=request.POST.get('result_selected_subject'))
        result_exam_type=request.POST.get('result_exam_type')
        schedule_exam_type=ExamDetails.objects.filter(institute=request.user.profile.institute)
        institute_pk = request.user.profile.institute.pk
        if result_exam_type==None:
                    etype=ExamType.objects.get(institute= request.user.profile.institute, exam_type=result_exam_type)
                    exam_type=etype.id
                    result_exam_type=exam_type
        exam_type_id=ExamType.objects.get(pk=result_exam_type)
        result_exam_type_sr_no = request.POST.get('fetch_sr_no')
      #============================================================================================ 
        student_designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='student')
        institute_students = UserProfile.objects.filter(institute= request.user.profile.institute, designation=student_designation_pk,Class=selected_subject.subject_class)
        exam_details = ExamDetails.objects.filter(institute=request.user.profile.institute, exam_type__exam_type= exam_type_id,exam_sr_no= result_exam_type_sr_no,exam_class__name=selected_subject.subject_class )
        # score test
        for student in institute_students:
          try:
            student_score=ExamResult.objects.get(institute= request.user.profile.institute,result_subject=selected_subject, exam_type=exam_type_id,
             exam_sr_no=result_exam_type_sr_no, result_student_data=student.user)
            student.existing_marks=student_score.result_score
          except:
            pass
            
        if exam_details:
          context={
                    'subject_result':subject_result,
                    
                    'selected_subject':selected_subject,
                    'exam_type_id':exam_type_id,
                    'result_exam_type_sr_no':result_exam_type_sr_no,
                    'institute_exam_type':institute_exam_type,
                    'institute_students':institute_students,
                    
                    }
          return render(request, 'teacher_view.html', context) 
        else:
              messages.info(request, 'There is no schedule created for this selection!')
                 
              return HttpResponseRedirect(f'/examresult/examresult/{institute_pk}')    
    # ----------------------------------------------------------------------------------------------
      context={
                  'subject_result':subject_result,
                  'institute_exam_type':institute_exam_type,
                  }
      return render(request, 'teacher_view.html', context)    
  else:
        raise PermissionDenied
    
def examresult(request,pk):
    # starting user notice
      if request.user.profile.designation:
                request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
        # ending user notice
      result_institute=Institute.objects.get(pk=pk)
      exam_result_institute=ExamResult.objects.filter(institute=result_institute)
      inst_id=request.user.profile.institute.id
      #  to fetch the logged in  subject teacher
      subject_result=Subjects.objects.filter(institute=request.user.profile.institute, subject_teacher=request.user)
      institute_exam_type=ExamType.objects.filter(institute=request.user.profile.institute)
      if request.method=="POST":
          for sdata,score in zip(request.POST.getlist('student_first_name'),request.POST.getlist('student_marks')):
            student_data = User.objects.get(pk=sdata)
            exam_subject=Subjects.objects.get(pk=request.POST.get('selected_subject'))
            examtype=ExamType.objects.get(pk=request.POST.get('exam_type_id'))
            examsrno=request.POST.get('result_exam_type_sr_no')
            subject_class=Classes.objects.get(pk=request.POST.get('subject_class'))
            subject_teacher=User.objects.get(pk=request.POST.get('subject_teacher'))
            exam_max_marks=request.POST.get('exam_max_marks')
            exam_max_limit=request.POST.get('exam_max_limit')
            try:
              
              st_data=ExamResult.objects.get(institute= request.user.profile.institute,result_subject=exam_subject, exam_type=examtype,
              exam_sr_no=examsrno, result_student_data=student_data)
              st_data.result_score=score
              st_data.save()
            except:
              marks_data=ExamResult()
              marks_data.institute=request.user.profile.institute
              marks_data.exam_sr_no= examsrno
              marks_data.result_student_data=student_data
              marks_data.exam_type= examtype
              marks_data.result_subject=exam_subject
              marks_data.result_class=subject_class
              marks_data.result_subject_teacher=subject_teacher
              marks_data.result_score=score
              marks_data.result_max_marks=exam_max_marks
              marks_data.save()

          marks_list=[]
          exam_result_data=ExamResult.objects.filter(institute=request.user.profile.institute,exam_type__exam_type=examtype,result_subject=exam_subject,exam_sr_no=examsrno)
          exam_subject=CalculateResult.objects.filter(institute=request.user.profile.institute, calc_result_student_data=request.user)
            
          for marks in exam_result_data:

                marks_list.append(marks.result_score)
          
                data_list=list( marks_list)
                marks_list=list(map(int, data_list))
                check_limit=int(exam_max_marks)
          for score in marks_list:
                  if score<check_limit or score==check_limit:
                              pass
                  else:
                              messages.info(request, 'Entered Marks is greater than the Exam Type Maximum Marks')
                              return redirect(f'/examresult/examresult/{inst_id}')
              
          messages.success(request, 'Exam Result Stored successfully !!!')  
          return redirect(f'/examresult/examresult/{inst_id}') 

      
# Student View
def student_view(request,pk):
    student=UserProfile.objects.filter(user=request.user)
    if request.method=="POST":
        result_exam_type = request.POST.get('chart_exam_type')
        result_exam_type_sr_no = request.POST.get('chart_sr_no')
        student_marks=[]
        student_subject=[]
        student_view=ExamResult.objects.filter(institute=request.user.profile.institute,result_student_data=request.user, exam_type__exam_type=result_exam_type,exam_sr_no=result_exam_type_sr_no)
        for marks in student_view:
            student_marks.append(marks.result_score)
        student_marks_data=list(student_marks)
       
        for subjects in student_view:
          student_subject.append(subjects.result_subject)
        student_subject_data=list(student_subject)
        context={
              'student_view':student_view,
              'student_marks':student_marks_data,
              'student_subject':student_subject_data,
              

                }
        return render(request, 'studentview.html', context)
   
    institute_exam_type=ExamType.objects.filter(institute=request.user.profile.institute)
    context={
      'institute_exam_type':institute_exam_type,
            }
    return render(request, 'studentview.html' , context)




def fetch_sr_no(request):
  exam_type_id = request.POST.get('exam_type_id')
  exam_type=ExamType.objects.get(pk=exam_type_id)
  max_exam_sr_no = ExamDetails.objects.filter(exam_type=exam_type).values('exam_sr_no').distinct()
  individual_result_sr_no = "<option>--Exam Type No.--</option>"
  for result_sr_no in max_exam_sr_no:
    individual_result_sr_no = individual_result_sr_no + f"<option value='{result_sr_no['exam_sr_no']}'>"+result_sr_no['exam_sr_no']+"</option>" 
  return HttpResponse(individual_result_sr_no)




def chart_sr_no(request):
  exam_type_id = request.POST.get('exam_type_id')
  
  max_exam_sr_no = ExamResult.objects.filter(exam_type__exam_type=exam_type_id).values('exam_sr_no').distinct()
  chart_result_sr_no = "<option>--Exam Type No.--</option>"
  for result_sr_no in max_exam_sr_no:
    chart_result_sr_no = chart_result_sr_no + f"<option>"+result_sr_no['exam_sr_no']+"</option>" 
  return HttpResponse(chart_result_sr_no)

def report_card(request,pk):
      user_institute_name=Institute.objects.get(pk=pk)
        # starting user notice
      if request.user.profile.designation:
                request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
        # ending user notice

      request.user.user_child_fee_status = []
      user_children= AddChild.objects.filter(parent= request.user.profile)
      parent_student_list = []
      for st in user_children:
            student= UserProfile.objects.get(pk=st.child.id)
            parent_student_list.append(student)
      exam_type_list =ExamType.objects.filter(institute=request.user.profile.institute)
      exam_id=request.user.profile.institute.id

      if request.method=="POST":
          if request.user.profile.designation.level_name=='student':
              institute_student=request.user.profile.institute
              selected_student=request.user
              
              student_class=request.user.profile.Class
              student_session_start=request.user.profile.class_current_year
              student_session_end=request.user.profile.class_next_year
              student_profile_pic=request.user.profile.profile_pic
              student_roll_no=request.user.profile.roll_number
              student_first_name=request.user.profile.first_name
              student_last_name=request.user.profile.last_name
              student_mother_name=request.user.profile.mother_name
              student_father_name=request.user.profile.father_name
              student_dob=request.user.profile.date_of_birth
              student_contact_no=request.user.profile.mobile_number
              student_address1=request.user.profile.address_line_1
              student_address2=request.user.profile.address_line_2
              # student_session=UserProfile.objects.get(pk=request.user)
              select_exam_type = request.POST.get('result_exam_type')
              if select_exam_type=="overall":
                if request.POST.get("report_cart_button"):
                    # return HttpResponseRedirect(f'/examresult/overall_report_card/{exam_id}/{selected_student.id}')
                  return overall_report_card(request,exam_id,selected_student.id)


                else:
                   
                    # return overall_result(request,exam_id,selected_student.id)

                     return HttpResponseRedirect(f'/examresult/overall_result/{exam_id}/{selected_student.id}')

                  # return HttpResponseRedirect(f'/examresult/overall_result/{exam_id}/{request.user.id}')
              else :
                if select_exam_type!="overall":
                  
                    if request.POST.get("report_cart_button"):
                      return reports_card(request,exam_id)
                      # return HttpResponseRedirect(f'/examresult/reports_card/{exam_id}')

                    elif request.POST.get("view_button"):
                      pass
                
              exam_type=ExamType.objects.get(pk=select_exam_type)
              exam_per_value=exam_type.exam_per_final_score
              e=int(exam_per_value)
              e_maxmarks=exam_type.exam_max_marks
              examtype_maxmarks=int(e_maxmarks)
              e_total_limit=exam_type.exam_max_limit
              examtype_total_limit=int(e_total_limit)

              all_exam=ExamResult.objects.filter(exam_type=exam_type,result_student_data=request.user)
              exam_no=[]
              for data in all_exam:
                if data.exam_sr_no in exam_no:
                  pass
                else:
                  exam_no.append(data.exam_sr_no)
              resultsubject=[]
              for sub in all_exam:
                if sub.result_subject in resultsubject:
                  pass
                else:
                  resultsubject.append(sub.result_subject)
              result_data=[]
              for sub_data in resultsubject:
                data_marks={}
                data_marks['subj']=sub_data
                
                s=sub_data
                for e_no in exam_no:
                  try:
                        student_data=ExamResult.objects.get(exam_type=exam_type,exam_sr_no=e_no, result_student_data=request.user,result_subject=sub_data)
                        data_marks[e_no]=student_data.result_score
                        
                  except: 
                      data_marks[e_no]=None
                marks_data=[]
                for key,value in data_marks.items():
                    if key=="subj":
                      pass
                    else:
                      marks_data.append(value)
                sum=0
                for m in marks_data:
                    if m is None: 
                      pass
                    else:
                      sum= sum+m
                max_exam_limit=exam_no[-1]  
                max_limit=int(max_exam_limit)  
                sumValue=sum
                data_marks['sum']=sumValue
                sumper=((sumValue/max_limit)/examtype_maxmarks)*e
                data_marks['avg']=round(sumper,2)
                result_data.append(data_marks)
                percentage_sum=[]
                for k,v in data_marks.items():
                    if k=='avg':
                      percentage_sum.append(v)
                sum=0
                for per_sum in percentage_sum:
                    sum=sum+per_sum
              context={
                'user_institute_name':user_institute_name,
                'institute_student':institute_student,
                'student_class':student_class,
                    'select_exam_type':exam_type,
                    'all_exam':all_exam,
                    'exam_no':exam_no,
                    'resultsubject':resultsubject,
                    'result_data':result_data,
                    'exam_type_list':exam_type_list,
                    'parent_student_list':parent_student_list,
                    'e_maxmarks':e_maxmarks,
                          }
              return render(request, 'report_card.html', context)

      context={
        'user_institute_name':user_institute_name,
            'exam_type_list':exam_type_list,
            'parent_student_list':parent_student_list,
            
          }

      return render(request, 'report_card.html', context)
        

            
      if request.user.profile.designation.level_name=='parent':
            if request.method=="POST":
              user_institute_name=Institute.objects.get(pk=pk)
              select_exam_type = request.POST.get('result_exam_type')
              select_st= request.POST.get('selected_student')
              selected_student=UserProfile.objects.get(pk=select_st)
              student_class= selected_student.Class
              institute_student=selected_student.institute
              student_session_start=selected_student.class_current_year
              student_session_end=selected_student.class_next_year
              student_profile_pic=selected_student.profile_pic
              student_roll_no=selected_student.roll_number
              student_first_name=selected_student.first_name
              student_last_name=selected_student.last_name
              student_mother_name=selected_student.mother_name
              student_father_name=selected_student.father_name
              student_dob=selected_student.date_of_birth
              student_contact_no=selected_student.mobile_number
              student_address1=selected_student.address_line_1
              student_address2=selected_student.address_line_2
              exam_id=request.user.profile.institute.id
              # if select_exam_type=="Overall":
              #   # return render(request, 'overall.html', context)
              #   return HttpResponseRedirect(f'/examresult/overall_result/{exam_id}/{selected_student.id}')
              
              if select_exam_type=="overall":
                if request.POST.get("report_cart_button"):
                    return HttpResponseRedirect(f'/examresult/overall_report_card/{exam_id}/{select_st}')

                  # return overall_report_card(request,exam_id,select_st)

                elif request.POST.get("view_button"):
                     return HttpResponseRedirect(f'/examresult/overall_result/{exam_id}/{select_st}')

                  # return overall_result(request,exam_id,select_st)
              else :
                if select_exam_type!="overall":
                  
                    if request.POST.get("report_cart_button"):
                      return reports_card(request,exam_id)

                    elif request.POST.get("view_button"):
                      pass 
              exam_type=ExamType.objects.get(pk=select_exam_type)
              exam_per_value=exam_type.exam_per_final_score
              e=int(exam_per_value)
              e_maxmarks=exam_type.exam_max_marks
              examtype_maxmarks=int(e_maxmarks)
              e_total_limit=exam_type.exam_max_limit
              examtype_total_limit=int(e_total_limit)
              
              all_exam=ExamResult.objects.filter(exam_type=exam_type,result_student_data=selected_student.id)
              exam_no=[]
              for data in all_exam:
                if data.exam_sr_no in exam_no:
                  pass
                else:
                  exam_no.append(data.exam_sr_no)
              resultsubject=[]
              for sub in all_exam:
                if sub.result_subject in resultsubject:
                  pass
                else:
                  resultsubject.append(sub.result_subject)
              result_data=[]
              for sub_data in resultsubject:
                data_marks={}
              
                data_marks['subj']=sub_data
                for e_no in exam_no:
                  try:
                    student_data=ExamResult.objects.get(exam_type=exam_type,exam_sr_no=e_no, result_student_data=selected_student,result_subject=sub_data)
                    data_marks[e_no]=student_data.result_score
                  except:
                    data_marks[e_no]=None
                marks_data=[]
                for key,value in data_marks.items():
                    if key=="subj":
                      pass
                    else:
                      marks_data.append(value)
                sum=0
                for m in marks_data:
                    if m is None: 
                      pass
                    else:
                      sum= sum+m

                max_exam_limit=exam_no[-1]  
                max_limit=int(max_exam_limit)  
                sumValue=sum
                data_marks['sum']=sumValue
                sumper=((sumValue/max_limit)/examtype_maxmarks)*e
                data_marks['avg']=round(sumper,2)
                result_data.append(data_marks)
                percentage_sum=[]
                for k,v in data_marks.items():
                    if k=='avg':
                      percentage_sum.append(v)
                sum=0
                for per_sum in percentage_sum:
                    sum=sum+per_sum

                

              context={
                'user_institute_name':user_institute_name,
                'e_maxmarks':e_maxmarks,
                    'institute_student':institute_student,
                    'student_class':student_class,
                    'select_exam_type':exam_type,
                    'all_exam':all_exam,
                    'exam_no':exam_no,
                    'resultsubject':resultsubject,
                    'result_data':result_data,
                    'exam_type_list':exam_type_list,
                    'parent_student_list':parent_student_list,
                    'student_session_start':student_session_start,
                    'student_session_end':student_session_end,
                    'student_profile_pic':student_profile_pic,
                    'student_roll_no':student_roll_no,
                    'student_first_name':student_first_name,
                    'student_last_name':student_last_name,
                    'student_mother_name':student_mother_name,
                    'student_father_name':student_father_name,
                    'student_dob':student_dob,
                    'student_contact_no':student_contact_no,
                    'student_address1':student_address1,
                    'student_address2':student_address2,
                          }
              return render(request, 'report_card.html', context)        
      context={
        'user_institute_name':user_institute_name,
            'exam_type_list':exam_type_list,
            'parent_student_list':parent_student_list,
            
          }

      return render(request, 'report_card.html', context)
        




def overall_result(request,pk,student_pk):
  inst = request.user.profile.institute.id
  user_children= AddChild.objects.filter(parent= request.user.profile)
  parent_student_list = []
  for st in user_children:
            student= UserProfile.objects.get(pk=st.child.id)
            parent_student_list.append(student)
  user_institute_name=Institute.objects.get(pk=pk)
  selected_student_data=UserProfile.objects.get(pk=student_pk)
  institute_student=selected_student_data.institute
  student_class=selected_student_data.Class

  if pk==inst:
    if request.user.profile.designation.level_name=='parent':
      if request.method=="POST":
              user_institute_name=Institute.objects.get(pk=pk)
              select_exam_type = request.POST.get('result_exam_type')
              select_st=request.POST.get('selected_student')
              selected_student=User.objects.get(pk=select_st)
              student_class= selected_student.profile.Class
              institute_student=selected_student.profile.institute

              exam_id=request.user.profile.institute.id


             
              # if select_exam_type=="Overall":
               
              #   # return render(request, 'overall.html', context)

              #   return HttpResponseRedirect(f'/examresult/overall_result/{exam_id}/{selected_student.id}')
              
              if select_exam_type=="overall":
                select_exam_type = request.POST.get('result_exam_type')
                select_st=request.POST.get('selected_student')
                selected_student=UserProfile.objects.get(pk=select_st)
                if request.POST.get("report_cart_button"):
                  return HttpResponseRedirect(f'/examresult/overall_report_card/{exam_id}/{selected_student.id}')

                elif request.POST.get("view_button"):
                  return HttpResponseRedirect(f'/examresult/overall_result/{exam_id}/{selected_student.id}')
              else :
                if select_exam_type!="overall":
                    print("overall inside")
                  
                    if request.POST.get("report_cart_button"):
                      return reports_card(request,exam_id)
                      # return HttpResponseRedirect(f'/examresult/reports_card/{exam_id}')

                    elif request.POST.get("view_button"):
                       return report_card(request,exam_id)
                      
              exam_type=ExamType.objects.get(pk=select_exam_type)
              exam_per_value=exam_type.exam_per_final_score
              e=int(exam_per_value)
              e_maxmarks=exam_type.exam_max_marks
              examtype_maxmarks=int(e_maxmarks)
              e_total_limit=exam_type.exam_max_limit
              examtype_total_limit=int(e_total_limit)
              
              all_exam=ExamResult.objects.filter(exam_type=exam_type,result_student_data=selected_student)
              exam_no=[]
              for data in all_exam:
                if data.exam_sr_no in exam_no:
                  pass
                else:
                  exam_no.append(data.exam_sr_no)
              resultsubject=[]
              for sub in all_exam:
                if sub.result_subject in resultsubject:
                  pass
                else:
                  resultsubject.append(sub.result_subject)
              result_data=[]
              for sub_data in resultsubject:
                data_marks={}
              
                data_marks['subj']=sub_data
                for e_no in exam_no:
                  try:
                    student_data=ExamResult.objects.get(exam_type=exam_type,exam_sr_no=e_no, result_student_data=selected_student,result_subject=sub_data)
                    data_marks[e_no]=student_data.result_score
                  except:
                    data_marks[e_no]=None
                marks_data=[]
                for key,value in data_marks.items():
                    if key=="subj":
                      pass
                    else:
                      marks_data.append(value)
                sum=0
                for m in marks_data:
                    if m is None: 
                      pass
                    else:
                      sum= sum+m

                max_exam_limit=exam_no[-1]  
                max_limit=int(max_exam_limit)  
                sumValue=sum
                data_marks['sum']=sumValue
                sumper=((sumValue/max_limit)/examtype_maxmarks)*e
                data_marks['avg']=round(sumper,2)
                result_data.append(data_marks)
                percentage_sum=[]
                for k,v in data_marks.items():
                    if k=='avg':
                      percentage_sum.append(v)
                sum=0
                for per_sum in percentage_sum:
                    sum=sum+per_sum

                

              context={
                'user_institute_name':user_institute_name,
                'e_maxmarks':e_maxmarks,
                    'institute_student':institute_student,
                    'student_class':student_class,
                    'select_exam_type':exam_type,
                    'all_exam':all_exam,
                    'exam_no':exam_no,
                    'resultsubject':resultsubject,
                    'result_data':result_data,
                    'exam_type_list':exam_type_list,
                    'parent_student_list':parent_student_list,
                    'selected_student':selected_student,
                          }
              return render(request, 'report_card.html', context)        
      context={
          'user_institute_name':user_institute_name,
              
              'parent_student_list':parent_student_list,
              
            }

      return render(request, 'report_card.html', context)
                 


    if request.user.profile.designation.level_name=='student':
      user_institute_name=Institute.objects.get(pk=pk)
      institute_student=request.user.profile.institute
      student_class=request.user.profile.Class
      select_exam_type = request.POST.get('result_exam_type')
      selected_student=request.user
      exam_id=request.user.profile.institute.id
      
      if select_exam_type=="overall":
         
          if request.POST.get("report_cart_button"):
              return HttpResponseRedirect(f'/examresult/overall_report_card/{exam_id}/{selected_student.id}')

          elif request.POST.get("view_button"):
              return HttpResponseRedirect(f'/examresult/overall_result/{exam_id}/{selected_student.id}')
      else :
            if select_exam_type!="overall":
                  
              if request.POST.get("report_cart_button"):
                  return reports_card(request,exam_id)
                      # return HttpResponseRedirect(f'/examresult/reports_card/{exam_id}')

              elif request.POST.get("view_button"):
                  return report_card(request,exam_id)

                    # return HttpResponseRedirect(f'/examresult/report_card/{exam_id}')

                  # return redirect('report_card')
      # Create the list of all exam type present in the institute
      type_exam=[]
      exam_type_list=ExamType.objects.filter(institute=request.user.profile.institute)
      for exam in exam_type_list:
        type_exam.append(exam)
      count_value=0
      for exam_count in type_exam:
        count_value=count_value+1


      for exam_type in exam_type_list:
        exam_data= ExamResult.objects.filter(exam_type=exam_type,result_student_data=request.user)

        # list of all sr no
        exam_no=[]
        for data in exam_data:
          if data.exam_sr_no in exam_no:
            pass
          else:
            exam_no.append(data.exam_sr_no)
        # print(exam_no)

        #  list of all subjects  
        resultsubject=[]
        for sub in exam_data:
          if sub.result_subject in resultsubject:
            pass
          else:
            resultsubject.append(sub.result_subject)
        
       

        
        e_data=[]
        for etype in type_exam:
          etype_limit=etype.exam_max_limit
          exam_type_limit=int(etype_limit)
          etype_marks=etype.exam_max_marks
          exam_type_marks=int(etype_marks)
          # final score based on exam type
          e_type_perValue=etype.exam_per_final_score
          e_type_per=int(e_type_perValue)
      
          for sub in resultsubject:
            # create list to store exam result
              e_score=[]
            # dictionary to store all data set
              dict1={}
              # store subjects in dictionary
              dict1['sub']=sub
              # store data type in dictionary
              dict1['etype']=etype
              # fetch the value of exam score
              for eno in exam_no:
                  examresult_data=ExamResult.objects.filter(exam_type=etype,result_subject=sub,exam_sr_no=eno,result_student_data=request.user)
                  for exam_score in examresult_data:
                      e_score.append(exam_score.result_score)
                  marks_list=list(e_score)
                        
               
              # print(max_limit)
              max_sr_value=[]
           
              max_exam_sr_no = ExamDetails.objects.filter(exam_type=etype).values('exam_sr_no').distinct()
              for max_value in max_exam_sr_no:
                  for k,v in max_value.items():
                        max_sr_value.append(v)
           
             
                    # print(v)
              try:
                  max_exam_limit=max_sr_value[-1]  
                  max_limit=int(max_exam_limit)
              except:
                max_exam_limit=None
                max_limit=1
              
              # for loop in exam score list
              sum=0
              for score in e_score:  
                  sum=sum+score
              sumValue=sum
               
              perValue=(sumValue/max_limit/exam_type_marks)*e_type_per
              # store percent in dictionary
              dict1['percent']=round(perValue,2)
              e_data.append(dict1)
        
        
        # retrieve list of all subjects from dictionary
        sub_value=[]
        for eytpe in e_data:
          for sub in e_data:
              for k,v in sub.items():
                  if k=='sub':
                    if v in sub_value:
                      pass
                    else:
                      sub_value.append(v)
        
       # retrieve list of all percentage from dictionary
        sub_percent_list=[]
        for subject in sub_value:
          sub_percent={}
          all_percent_list=[]
          per={}
          for sub in e_data:
            sub_percent['sub']=subject
            for k,v in sub.items():
              if k=='sub' and v==subject:
                 
                 for k,v in sub.items():
                   if k=='percent':
                     all_percent_list.append(v)
          # print(all_percent_list)
          for percent_marks in all_percent_list:
            sub_percent[percent_marks]=percent_marks 
          
          sum=0
          for percent in all_percent_list:
            sum=sum+percent
          sub_percent['percent_sum']=round(sum,2)
          sub_percent_list.append(sub_percent)
        final_percentage=[]
        for final_percent_sum in sub_percent_list:
            for k,v in final_percent_sum.items():
              if k=='percent_sum':
                final_percentage.append(v)
        sum=0
        for final_sum in final_percentage:
          sum=sum+final_sum
        # count the number of subjects
        count=0
        for i in resultsubject:
            count=count+1
        total_marks_count=count*100

        final_percent_result=(sum/total_marks_count)*100
        grand_result=round(final_percent_result,2)
        range_value=range(0, count_value)

        context={
          'institute_student':institute_student,
          'student_class':student_class,
        'user_institute_name':user_institute_name,
        'e_data':e_data,
        'type_exam':type_exam,
        'exam_type':exam_type,
        'etype':etype,
        'all_percent_list':all_percent_list,
        'exam_type_list':exam_type_list,
        'sub_percent_list':sub_percent_list,
        'grand_result':grand_result,
        'count_value':count_value,
        'range_value':range_value,
        'student_pk':request.user.id
        

        } 
        return render(request, 'overall.html', context)

            
    context={
        'exam_type_list':exam_type_list,
        
        } 
    return render(request, 'overall.html', context)
  else:
        raise PermissionDenied

  

  


  
  
def class_promotion(request,pk):
  inst = request.user.profile.institute.id

  if pk==inst:
        current_year=datetime.date.today().year
        next_year=datetime.date.today().year+1
        
        # to get the list of all  classes                                        
        all_classes = Classes.objects.filter(institute= request.user.profile.institute,class_teacher=request.user)
        promotes_class=Classes.objects.filter(institute= request.user.profile.institute)
        # to ge the data through POST method
        if request.method=="POST":
            selected_class_promotes =request.POST.get('selected_class_promotion')
            if selected_class_promotes == None:
                            first_class = Classes.objects.filter(institute= request.user.profile.institute).first()
                            first_class_id = first_class.id
                            selected_class_promotes= first_class_id
            selected_class = Classes.objects.get(pk=selected_class_promotes)
            #  to get the list of all students of selected class
            all_students = UserProfile.objects.filter(institute= request.user.profile.institute, Class= selected_class, designation__level_name='student', class_current_year=current_year)
            for student_class in all_students:
                  stu_class=student_class.Class
            promotion_status = UserProfile._meta.get_field('class_promotion_status').choices
            promotion_choices=dict(promotion_status)
            list_promotion_choices=list(promotion_choices)
            institute=request.user.profile.institute
            if request.method=="POST":
                      promoted_to_class=request.POST.get('promoted_to_class')
                      if promoted_to_class == None:
                            first_class = Classes.objects.filter(institute= request.user.profile.institute).first()
                            first_class_id = first_class.id
                            promoted_to_class= first_class_id
                      promoted_to_class = Classes.objects.get(pk=promoted_to_class)
                  #  to get the students data from the UserProfile
                      user_data=UserProfile.objects.filter(institute=institute, Class=selected_class)
                      #   get the list of users from the UserProfile
                      for user_d in user_data:
                          user_da=user_d.user
                      #  fetch the data from the front end
                          for sdata,status in zip(request.POST.getlist('student_roll_no'),request.POST.getlist('student_promotion_status')):
                            student_data = User.objects.get(pk=sdata)
                            if student_data==user_da:
                                  user_d.class_promotion_status=status
                                  if status=="Promoted":
                                    user_d.Class=promoted_to_class
                                    user_d.class_current_year=current_year+1
                                    user_d.class_next_year=next_year+1
                                  else:
                                    pass
                                  
                                  user_d.save()
              # Inner Context
            context= {
                'all_classes': all_classes,
                'all_students':all_students,
                'list_promotion_choices':list_promotion_choices,
                'promotes_class':promotes_class,
            }
            messages.success(request, 'Students Promoted successfully')
            return render(request, 'class_promotion.html', context)
        # Outer Context
        context= {
            'all_classes': all_classes,
            
        }
         
        return render(request, 'class_promotion.html', context)

  else:
        raise PermissionDenied

def st_result(request):
  
  pass
 


def render_to_pdf(template_src, context_dict={}):
      for i in context_dict.items():
        print(type(i))
      
      template=get_template(template_src)
      html = template.render(context_dict)
      result=BytesIO()
      pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)

      if not pdf.err:
          return HttpResponse(result.getvalue(),content_type='application/pdf')
      return None







def reports_card(request,pk):
      user_institute_name=Institute.objects.get(pk=pk)
        # starting user notice
      if request.user.profile.designation:
                request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
        # ending user notice

      request.user.user_child_fee_status = []
      user_children= AddChild.objects.filter(parent= request.user.profile)
      parent_student_list = []
      for st in user_children:
            student= UserProfile.objects.get(pk=st.child.id)
            parent_student_list.append(student)
      exam_type_list =ExamType.objects.filter(institute=request.user.profile.institute)
      exam_id=request.user.profile.institute.id

      if request.method=="POST":
          if request.user.profile.designation.level_name=='student':
              institute_student=request.user.profile.institute
              student_class=request.user.profile.Class
              student_session_start=request.user.profile.class_current_year
              student_session_end=request.user.profile.class_next_year
              student_profile_pic=request.user.profile.profile_pic
              student_roll_no=request.user.profile.roll_number
              student_first_name=request.user.profile.first_name
              student_last_name=request.user.profile.last_name
              student_mother_name=request.user.profile.mother_name
              student_father_name=request.user.profile.father_name
              student_dob=request.user.profile.date_of_birth
              student_contact_no=request.user.profile.mobile_number
              student_address1=request.user.profile.address_line_1
              student_address2=request.user.profile.address_line_2
              student_profile_pic =request.user.profile.profile_pic
              # student_session=UserProfile.objects.get(pk=request.user)
              select_exam_type = request.POST.get('result_exam_type')
              if select_exam_type=="Overall":
                if request.POST.get("report_cart_button"):
                  return HttpResponseRedirect(f'/examresult/overall_report_card/{exam_id}/{request.user.id}')

                elif request.POST.get("view_button"):
                  return HttpResponseRedirect(f'/examresult/overall_result/{exam_id}/{request.user.id}')

              exam_type=ExamType.objects.get(pk=select_exam_type)
              exam_per_value=exam_type.exam_per_final_score
              e=int(exam_per_value)
              e_maxmarks=exam_type.exam_max_marks
              examtype_maxmarks=int(e_maxmarks)
              e_total_limit=exam_type.exam_max_limit
              examtype_total_limit=int(e_total_limit)

              all_exam=ExamResult.objects.filter(exam_type=exam_type,result_student_data=request.user)
              exam_no=[]
              for data in all_exam:
                if data.exam_sr_no in exam_no:
                  pass
                else:
                  exam_no.append(data.exam_sr_no)
              resultsubject=[]
              for sub in all_exam:
                if sub.result_subject in resultsubject:
                  pass
                else:
                  resultsubject.append(sub.result_subject)
              result_data=[]
              for sub_data in resultsubject:
                data_marks={}
                data_marks['subj']=sub_data
                
                s=sub_data
                for e_no in exam_no:
                  try:
                        student_data=ExamResult.objects.get(exam_type=exam_type,exam_sr_no=e_no, result_student_data=request.user,result_subject=sub_data)
                        data_marks[e_no]=student_data.result_score
                        
                  except: 
                      data_marks[e_no]=None
                my_session_context={}
               

                marks_data=[]
                for key,value in data_marks.items():
                    if key=="subj":
                      pass
                    else:
                      marks_data.append(value)
                sum=0
                for m in marks_data:
                    if m is None: 
                      pass
                    else:
                      sum= sum+m
                
           

                max_exam_limit=exam_no[-1]  
                max_limit=int(max_exam_limit)  
                sumValue=sum
                data_marks['sum']=sumValue
                sumper=((sumValue/max_limit)/examtype_maxmarks)*e
                data_marks['avg']=round(sumper,2)
                result_data.append(data_marks)
                percentage_sum=[]
                for k,v in data_marks.items():
                    if k=='avg':
                      percentage_sum.append(v)
                sum=0
                for per_sum in percentage_sum:
                    sum=sum+per_sum
              
              


              context={
                'user_institute_name':user_institute_name,
                'institute_student':institute_student,
                'student_roll_no':student_roll_no,
                'student_first_name':student_first_name,
                'student_last_name':student_last_name,
                'student_father_name':student_father_name,
                'student_mother_name':student_mother_name,
                'student_dob':student_dob,
                'student_contact_no':student_contact_no,
                'student_address1':student_address1,
                'student_address2':student_address2,
                'student_profile_pic':student_profile_pic,
                'student_class':student_class,
                    'select_exam_type':exam_type,
                    'all_exam':all_exam,
                    'exam_no':exam_no,
                    'resultsubject':resultsubject,
                    'result_data':result_data,
                    'exam_type_list':exam_type_list,
                    'parent_student_list':parent_student_list,
                    'e_maxmarks':e_maxmarks,
                    'sum':sum,
                          }
              return render(request, 'ReportCard.html', context)

            
          if request.user.profile.designation.level_name=='parent':
              user_institute_name=Institute.objects.get(pk=pk)
              select_exam_type = request.POST.get('result_exam_type')
              selected_student=UserProfile.objects.get(pk=request.POST.get('selected_student'))
              student_class= selected_student.Class
              institute_student=selected_student.institute
              student_session_start=selected_student.class_current_year
              student_session_end=selected_student.class_next_year
              student_profile_pic=selected_student.profile_pic
              student_roll_no=selected_student.roll_number
              student_first_name=selected_student.first_name
              student_last_name=selected_student.last_name
              student_mother_name=selected_student.mother_name
              student_father_name=selected_student.father_name
              student_dob=selected_student.date_of_birth
              student_contact_no=selected_student.mobile_number
              student_address1=selected_student.address_line_1
              student_address2=selected_student.address_line_2

             
              if select_exam_type=="Overall":
                select_exam_type = request.POST.get('result_exam_type')
                selected_student=User.objects.get(pk=request.POST.get('selected_student'))

                # return render(request, 'overall.html', context)

                return HttpResponseRedirect(f'/examresult/overall_result/{exam_id}/{selected_student.id}')
              
              exam_type=ExamType.objects.get(pk=select_exam_type)
              exam_per_value=exam_type.exam_per_final_score
              e=int(exam_per_value)
              e_maxmarks=exam_type.exam_max_marks
              examtype_maxmarks=int(e_maxmarks)
              e_total_limit=exam_type.exam_max_limit
              examtype_total_limit=int(e_total_limit)
              
              all_exam=ExamResult.objects.filter(exam_type=exam_type,result_student_data=selected_student.id)
              exam_no=[]
              for data in all_exam:
                if data.exam_sr_no in exam_no:
                  pass
                else:
                  exam_no.append(data.exam_sr_no)
              resultsubject=[]
              for sub in all_exam:
                if sub.result_subject in resultsubject:
                  pass
                else:
                  resultsubject.append(sub.result_subject)
              result_data=[]
              for sub_data in resultsubject:
                data_marks={}
              
                data_marks['subj']=sub_data
                for e_no in exam_no:
                  try:
                    student_data=ExamResult.objects.get(exam_type=exam_type,exam_sr_no=e_no, result_student_data=selected_student.id,result_subject=sub_data)
                    data_marks[e_no]=student_data.result_score
                  except:
                    data_marks[e_no]=None
                marks_data=[]
                for key,value in data_marks.items():
                    if key=="subj":
                      pass
                    else:
                      marks_data.append(value)
                sum=0
                for m in marks_data:
                    if m is None: 
                      pass
                    else:
                      sum= sum+m

                max_exam_limit=exam_no[-1]  
                max_limit=int(max_exam_limit)  
                sumValue=sum
                data_marks['sum']=sumValue
                sumper=((sumValue/max_limit)/examtype_maxmarks)*e
                data_marks['avg']=round(sumper,2)
                result_data.append(data_marks)
                percentage_sum=[]
                for k,v in data_marks.items():
                    if k=='avg':
                      percentage_sum.append(v)
                sum=0
                for per_sum in percentage_sum:
                    sum=sum+per_sum

                

              context={
                    'user_institute_name':user_institute_name,
                    'student_roll_no':student_roll_no,
                    'student_first_name':student_first_name,
                    'student_last_name':student_last_name,
                    'student_father_name':student_father_name,
                    'student_mother_name':student_mother_name,
                    'student_dob':student_dob,
                    'student_contact_no':student_contact_no,
                    'student_address1':student_address1,
                    'student_address2':student_address2,
                    'student_profile_pic':student_profile_pic,
                    'student_class':student_class,
                    'e_maxmarks':e_maxmarks,
                    'institute_student':institute_student,
                    'student_class':student_class,
                    'select_exam_type':exam_type,
                    'all_exam':all_exam,
                    'exam_no':exam_no,
                    'resultsubject':resultsubject,
                    'result_data':result_data,
                    'exam_type_list':exam_type_list,
                    'parent_student_list':parent_student_list,
                          }
          return render(request, 'ReportCard.html', context)        
      context={
        'user_institute_name':user_institute_name,
            'exam_type_list':exam_type_list,
            'parent_student_list':parent_student_list,
            
          }

      return render(request, 'ReportCard.html', context)
        

def overall_report_card(request,pk,student_pk):
  inst = request.user.profile.institute.id
  user_institute_name=Institute.objects.get(pk=pk)
  selected_student_data=UserProfile.objects.get(pk=student_pk)
  institute_student=selected_student_data.institute
  student_class=selected_student_data.Class

  if pk==inst:
    if request.user.profile.designation.level_name=='parent':
      student_class= selected_student_data.Class
      institute_student=selected_student_data.institute
      student_session_start=selected_student_data.class_current_year
      student_session_end=selected_student_data.class_next_year
      student_profile_pic=selected_student_data.profile_pic
      student_roll_no=selected_student_data.roll_number
      student_first_name=selected_student_data.first_name
      student_last_name=selected_student_data.last_name
      student_mother_name=selected_student_data.mother_name
      student_father_name=selected_student_data.father_name
      student_dob=selected_student_data.date_of_birth
      student_contact_no=selected_student_data.mobile_number
      student_address1=selected_student_data.address_line_1
      student_address2=selected_student_data.address_line_2
      
      type_exam=[]
      exam_type_list=ExamType.objects.filter(institute=request.user.profile.institute)
      for exam in exam_type_list:
        type_exam.append(exam)
      count_value=0
      for exam_count in type_exam:
        count_value=count_value+1


      for exam_type in exam_type_list:
        exam_data= ExamResult.objects.filter(exam_type=exam_type,result_student_data=student_pk)

        # list of all sr no
        exam_no=[]
        for data in exam_data:
          if data.exam_sr_no in exam_no:
            pass
          else:
            exam_no.append(data.exam_sr_no)
        # print(exam_no)

        #  list of all subjects  
        resultsubject=[]
        for sub in exam_data:
          if sub.result_subject in resultsubject:
            pass
          else:
            resultsubject.append(sub.result_subject)
        
       

        
        e_data=[]
        for etype in type_exam:
          etype_limit=etype.exam_max_limit
          exam_type_limit=int(etype_limit)
          etype_marks=etype.exam_max_marks
          exam_type_marks=int(etype_marks)
          # final score based on exam type
          e_type_perValue=etype.exam_per_final_score
          e_type_per=int(e_type_perValue)
      
          for sub in resultsubject:
            # create list to store exam result
              e_score=[]
            # dictionary to store all data set
              dict1={}
              # store subjects in dictionary
              dict1['sub']=sub
              # store data type in dictionary
              dict1['etype']=etype
              # fetch the value of exam score
              for eno in exam_no:
                  examresult_data=ExamResult.objects.filter(exam_type=etype,result_subject=sub,exam_sr_no=eno,result_student_data=student_pk)
                  for exam_score in examresult_data:
                      e_score.append(exam_score.result_score)
                  marks_list=list(e_score)
                        
               
              # print(max_limit)
              max_sr_value=[]
              max_exam_sr_no = ExamDetails.objects.filter(exam_type=etype).values('exam_sr_no').distinct()
              for max_value in max_exam_sr_no:
                  for k,v in max_value.items():
                    max_sr_value.append(v)
                    # print(v)
              
              try:
                  max_exam_limit=max_sr_value[-1]  
                  max_limit=int(max_exam_limit)
              except:
                max_exam_limit=None
                max_limit=1
              
              # for loop in exam score list
              sum=0
              for score in e_score:  
                  sum=sum+score
              sumValue=sum
               
              perValue=(sumValue/max_limit/exam_type_marks)*e_type_per
              # store percent in dictionary
              dict1['percent']=round(perValue,2)
              e_data.append(dict1)
        # print(e_data)
        
        
        # retrieve list of all subjects from dictionary
        sub_value=[]
        for eytpe in e_data:
          for sub in e_data:
              for k,v in sub.items():
                  if k=='sub':
                    if v in sub_value:
                      pass
                    else:
                      sub_value.append(v)
        
      # retrieve list of all percentage from dictionary
        sub_percent_list=[]
        for subject in sub_value:
          sub_percent={}
          all_percent_list=[]
          per={}
          for sub in e_data:
            sub_percent['sub']=subject
            for k,v in sub.items():
              if k=='sub' and v==subject:
                 
                 for k,v in sub.items():
                   if k=='percent':
                     all_percent_list.append(v)
          # print(all_percent_list)
          for percent_marks in all_percent_list:
            sub_percent[percent_marks]=percent_marks 
          
          sum=0
          for percent in all_percent_list:
            sum=sum+percent
          sub_percent['percent_sum']=round(sum,2)
          sub_percent_list.append(sub_percent)
        final_percentage=[]
        for final_percent_sum in sub_percent_list:
            for k,v in final_percent_sum.items():
              if k=='percent_sum':
                final_percentage.append(v)
        sum=0
        for final_sum in final_percentage:
          sum=sum+final_sum
        # count the number of subjects
        count=0
        for i in resultsubject:
            count=count+1
        total_marks_count=count*100

        final_percent_result=(sum/total_marks_count)*100
        grand_result=round(final_percent_result,2)
        range_value=range(0, count_value)

        context={
          'institute_student':institute_student,
          'student_class':student_class,
        'user_institute_name':user_institute_name,
        'e_data':e_data,
        'type_exam':type_exam,
        'exam_type':exam_type,
        'etype':etype,
        'all_percent_list':all_percent_list,
        'exam_type_list':exam_type_list,
        'sub_percent_list':sub_percent_list,
        'grand_result':grand_result,
        'count_value':count_value,
        'range_value':range_value,
        'student_session_start':student_session_start,
        'student_session_end':student_session_end,
        'student_profile_pic':student_profile_pic,
        'student_roll_no':student_roll_no,
        'student_first_name':student_first_name,
        'student_last_name':student_last_name,
        'student_mother_name':student_mother_name,
        'student_father_name':student_father_name,
        'student_dob':student_dob,
        'student_contact_no':student_contact_no,
        'student_address1':student_address1,
        'student_address2':student_address2,
        

        } 
        return render(request, 'Overall_Report_Card.html', context)

            


    if request.user.profile.designation.level_name=='student':
      user_institute_name=Institute.objects.get(pk=pk)
      institute_student=request.user.profile.institute
      student_class=request.user.profile.Class
      student_session_start=request.user.profile.class_current_year
      student_session_end=request.user.profile.class_next_year
      student_profile_pic=request.user.profile.profile_pic
      student_roll_no=request.user.profile.roll_number
      student_first_name=request.user.profile.first_name
      student_last_name=request.user.profile.last_name
      student_mother_name=request.user.profile.mother_name
      student_father_name=request.user.profile.father_name
      student_dob=request.user.profile.date_of_birth
      student_contact_no=request.user.profile.mobile_number
      student_address1=request.user.profile.address_line_1
      student_address2=request.user.profile.address_line_2
      student_profile_pic =request.user.profile.profile_pic
      # Create the list of all exam type present in the institute
      type_exam=[]
      exam_type_list=ExamType.objects.filter(institute=request.user.profile.institute)
      for exam in exam_type_list:
        type_exam.append(exam)
      count_value=0
      for exam_count in type_exam:
        count_value=count_value+1


      for exam_type in exam_type_list:
        exam_data= ExamResult.objects.filter(exam_type=exam_type,result_student_data=request.user)

        # list of all sr no
        exam_no=[]
        for data in exam_data:
          if data.exam_sr_no in exam_no:
            pass
          else:
            exam_no.append(data.exam_sr_no)
        # print(exam_no)

        #  list of all subjects  
        resultsubject=[]
        for sub in exam_data:
          if sub.result_subject in resultsubject:
            pass
          else:
            resultsubject.append(sub.result_subject)
        
       

        
        e_data=[]
        for etype in type_exam:
          etype_limit=etype.exam_max_limit
          exam_type_limit=int(etype_limit)
          etype_marks=etype.exam_max_marks
          exam_type_marks=int(etype_marks)
          # final score based on exam type
          e_type_perValue=etype.exam_per_final_score
          e_type_per=int(e_type_perValue)
      
          for sub in resultsubject:
            # create list to store exam result
              e_score=[]
            # dictionary to store all data set
              dict1={}
              # store subjects in dictionary
              dict1['sub']=sub
              # store data type in dictionary
              dict1['etype']=etype
              # fetch the value of exam score
              for eno in exam_no:
                  examresult_data=ExamResult.objects.filter(exam_type=etype,result_subject=sub,exam_sr_no=eno,result_student_data=request.user)
                  for exam_score in examresult_data:
                      e_score.append(exam_score.result_score)
                  marks_list=list(e_score)
                        
               
              # print(max_limit)
              max_sr_value=[]
           
              max_exam_sr_no = ExamDetails.objects.filter(exam_type=etype).values('exam_sr_no').distinct()
              for max_value in max_exam_sr_no:
                  for k,v in max_value.items():
                        max_sr_value.append(v)
           
             
                    # print(v)
              try:
                  max_exam_limit=max_sr_value[-1]  
                  max_limit=int(max_exam_limit)
              except:
                max_exam_limit=None
                max_limit=1
              
              # for loop in exam score list
              sum=0
              for score in e_score:  
                  sum=sum+score
              sumValue=sum
               
              perValue=(sumValue/max_limit/exam_type_marks)*e_type_per
              # store percent in dictionary
              dict1['percent']=round(perValue,2)
              e_data.append(dict1)
        
        
        # retrieve list of all subjects from dictionary
        sub_value=[]
        for eytpe in e_data:
          for sub in e_data:
              for k,v in sub.items():
                  if k=='sub':
                    if v in sub_value:
                      pass
                    else:
                      sub_value.append(v)
        
      # retrieve list of all percentage from dictionary
        sub_percent_list=[]
        for subject in sub_value:
          sub_percent={}
          all_percent_list=[]
          per={}
          for sub in e_data:
            sub_percent['sub']=subject
            for k,v in sub.items():
              if k=='sub' and v==subject:
                 
                 for k,v in sub.items():
                   if k=='percent':
                     all_percent_list.append(v)
          # print(all_percent_list)
          for percent_marks in all_percent_list:
            sub_percent[percent_marks]=percent_marks 
          
          sum=0
          for percent in all_percent_list:
            sum=sum+percent
          sub_percent['percent_sum']=round(sum,2)
          sub_percent_list.append(sub_percent)
        final_percentage=[]
        for final_percent_sum in sub_percent_list:
            for k,v in final_percent_sum.items():
              if k=='percent_sum':
                final_percentage.append(v)
        sum=0
        for final_sum in final_percentage:
          sum=sum+final_sum
        # count the number of subjects
        count=0
        for i in resultsubject:
            count=count+1
        total_marks_count=count*100

        final_percent_result=(sum/total_marks_count)*100
        grand_result=round(final_percent_result,2)
        range_value=range(0, count_value)

        context={
          'institute_student':institute_student,
            'student_roll_no':student_roll_no,
                'student_first_name':student_first_name,
                'student_last_name':student_last_name,
                'student_father_name':student_father_name,
                'student_mother_name':student_mother_name,
                'student_dob':student_dob,
                'student_contact_no':student_contact_no,
                'student_address1':student_address1,
                'student_address2':student_address2,
                'student_profile_pic':student_profile_pic,
                'student_class':student_class,
          'student_class':student_class,
        'user_institute_name':user_institute_name,
        'e_data':e_data,
        'type_exam':type_exam,
        'exam_type':exam_type,
        'etype':etype,
        'all_percent_list':all_percent_list,
        'exam_type_list':exam_type_list,
        'sub_percent_list':sub_percent_list,
        'grand_result':grand_result,
        'count_value':count_value,
        'range_value':range_value,
        'exam_type_list':exam_type_list,
        

        } 
        return render(request, 'Overall_Report_Card.html', context)

            
    context={
        'exam_type_list':exam_type_list,
        
        } 
    return render(request, 'Overall_Report_Card.html', context)
  else:
        raise PermissionDenied

  

