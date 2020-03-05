from django.shortcuts import render
from .models import *
from main_app.models import *
from examschedule.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.db.models import Count

import statistics      






# Create your views here.
def exam_result(request,pk):
  # to fetch the current institute
  result_institute=Institute.objects.get(pk=pk)
  exam_result_institute=ExamResult.objects.filter(institute=result_institute)
  institute_exam_type=ExamType.objects.filter(institute=request.user.profile.institute)

  
  #  to fetch the logged in  subject teacher
  subject_result=Subjects.objects.filter(institute=request.user.profile.institute, subject_teacher=request.user)
  
 # to fetch the value of selected subject
  result_subject=request.GET.get('result_selected_subject')
  result_exam_type = request.GET.get('result_exam_type')
  result_exam_type_sr_no = request.GET.get('fetch_result_sr_no')
  if result_subject== None:
       first_subject=Subjects.objects.filter(institute= request.user.profile.institute).last()
       first_subject_id=first_subject.id 
       result_subject=first_subject_id
  selected_subject= Subjects.objects.get(pk=result_subject)
  
 
  # to fetch the institute students based on selected class 
  student_designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='student')
  institute_students = UserProfile.objects.filter(institute= request.user.profile.institute, designation=student_designation_pk,Class=selected_subject.subject_class)
 
  # to store the value of Exam Type

  
 # to get the data from the individual row
  if request.method=="POST":
      selected_exam_type =  ExamType.objects.filter(institute= request.user.profile.institute, exam_type= result_exam_type).first()
      for sdata,score in zip(request.POST.getlist('student_first_name'),request.POST.getlist('student_marks')):
         student_data = User.objects.get(pk=sdata)
         exam_max_marks=ExamType.objects.filter(institute=request.user.profile.institute, exam_type=result_exam_type)
        
         marks_data=ExamResult()
         marks_data.institute=request.user.profile.institute
         marks_data.exam_sr_no= result_exam_type_sr_no
         marks_data.exam_type= selected_exam_type
         marks_data.result_class=selected_subject.subject_class
         marks_data.result_subject=selected_subject
         marks_data.result_subject_teacher=selected_subject.subject_teacher
         marks_data.result_student_data=student_data
         marks_data.result_max_marks=selected_exam_type.exam_max_marks
         marks_data.result_score=score
         marks_data.save()
      marks_list=[]
      exam_result_data=ExamResult.objects.filter(institute=request.user.profile.institute,exam_type__exam_type=result_exam_type,result_subject=selected_subject,exam_sr_no=result_exam_type_sr_no)
      exam_subject=CalculateResult.objects.filter(institute=request.user.profile.institute, calc_result_student_data=request.user)
      
      for marks in exam_result_data:
          marks_list.append(marks.result_score)
     
      data_list=list(marks_list)
      marks_list=list(map(int, data_list))
      for subject in exam_result_data:
        subject=subject.result_subject
        print(subject)
      meanVal=statistics.mean(marks_list)

      maxValue=max(data_list)
      minValue=min(data_list)
      avgValue=round(meanVal)
      sumValue=sum(marks_list)
  
      for calc_data in exam_result_data:
          calculate_result=CalculateResult()
          calculate_result.institute=calc_data.institute
          calculate_result.calc_result_student_data=calc_data.result_student_data
          calculate_result.calc_result_subject=calc_data.result_subject
          calculate_result.calc_result_class=calc_data.result_class
          calculate_result.calc_result_exam_type=calc_data.exam_type
          calculate_result.calc_result_exam_sr_no=calc_data.exam_sr_no
          calculate_result.calc_result_score=calc_data.result_score
          calculate_result.calc_result_max=maxValue
          calculate_result.calc_result_min=minValue
          calculate_result.calc_result_avg=avgValue
          calculate_result.calc_result_total=sumValue
          calculate_result.save()
          
      messages.success(request, 'Exam Result Stored successfully !!!')

  context={

    'subject_result':subject_result,
    'selected_subject':selected_subject,
    'institute_students':institute_students,
    'institute_exam_type':institute_exam_type,
    
    }
  return render(request, 'teacher_view.html', context)


# Student View
def student_view(request,pk):
    student=UserProfile.objects.filter(user=request.user)
    if request.method=="POST":
        result_exam_type = request.POST.get('chart_exam_type')
        result_exam_type_sr_no = request.POST.get('chart_sr_no')
       
        student_view=ExamResult.objects.filter(institute=request.user.profile.institute,result_student_data=request.user, exam_type__exam_type=result_exam_type,exam_sr_no=result_exam_type_sr_no)
        context={
              'student_view':student_view,
                }
        return render(request, 'studentview.html', context)
   
    institute_exam_type=ExamType.objects.filter(institute=request.user.profile.institute)
    context={
      'institute_exam_type':institute_exam_type,
            }
    return render(request, 'studentview.html' , context)


def fetch_sr_no(request):
  exam_type_id = request.POST.get('exam_type_id')
  
  max_exam_sr_no = ExamDetails.objects.filter(exam_type__exam_type=exam_type_id).values('exam_sr_no').distinct()
  individual_result_sr_no = "<option>--Select Exam Type No.--</option>"
  for result_sr_no in max_exam_sr_no:
    individual_result_sr_no = individual_result_sr_no + f"<option>"+result_sr_no['exam_sr_no']+"</option>" 
    
  return HttpResponse(individual_result_sr_no)

def chart_sr_no(request):
  exam_type_id = request.POST.get('exam_type_id')
  
  max_exam_sr_no = ExamResult.objects.filter(exam_type__exam_type=exam_type_id).values('exam_sr_no').distinct()
  chart_result_sr_no = "<option>--Select Exam Type No.--</option>"
  for result_sr_no in max_exam_sr_no:
    chart_result_sr_no = chart_result_sr_no + f"<option>"+result_sr_no['exam_sr_no']+"</option>" 
    
  return HttpResponse(chart_result_sr_no)

def report_card(request,pk):

# get Exam Type
  exam_type_list =ExamType.objects.filter(institute=request.user.profile.institute)

  if request.method=="POST":
      select_exam_type = request.POST.get('result_exam_type')
      # exam_dataresult = ExamResult.objects.filter(institute=request.user.profile.institute, exam_type__exam_type= select_exam_type)
      exam_sr_no=ExamResult.objects.values('exam_sr_no').distinct()
      exam_data = ExamResult.objects.filter(institute=request.user.profile.institute, exam_type__exam_type= select_exam_type)
      max_marks=ExamType.objects.filter(institute=request.user.profile.institute, exam_type=select_exam_type)
      exam_subject = ExamResult.objects.filter(institute=request.user.profile.institute, exam_type__exam_type= select_exam_type)
      all_students_data=ExamResult.objects.filter(institute=request.user.profile.institute, exam_type__exam_type= select_exam_type )
      examresult_data=CalculateResult.objects.filter(institute=request.user.profile.institute,calc_result_student_data=request.user,calc_result_exam_type=select_exam_type)
      
      
      score_list=[]
      exam_rdata = ExamResult.objects.filter(institute=request.user.profile.institute,result_student_data=request.user, exam_type__exam_type= select_exam_type)
      
      for score in exam_rdata:
          score_list.append(score.result_score)

      scored_data=list(score_list)
      

      score_list=list(map(int, scored_data))
      
      
      meanVal=statistics.mean(score_list)

      round_score=round(meanVal)
      
      context={
        'exam_type_list':exam_type_list,
        'examresult_data':examresult_data,
        'exam_sr_no':exam_sr_no,
        'select_exam_type':select_exam_type,
        'exam_subject':exam_subject,
        'all_students_data':all_students_data,
        'max_marks':max_marks,
        'round_score':round_score,
              }
      return render(request, 'report_card.html', context)        
  context={
        'exam_type_list':exam_type_list,
        
        
      }

  return render(request, 'report_card.html', context)
  

def overall_result(request,pk):
    exam_type_list=ExamType.objects.filter(institute=request.user.profile.institute)
    exam_subjects=ExamResult.objects.filter(institute=request.user.profile.institute, result_student_data=request.user)
    for exam_sub in exam_subjects:
            subject=exam_sub.result_subject
            for exam_type in exam_type_list:
                    etype=exam_type.exam_type
                    exam_sr_no=ExamResult.objects.filter(exam_type__exam_type=etype).values('exam_sr_no').distinct()
                    for sr_no in exam_sr_no:
                      for key,value in sr_no.items():
                      
                                overall_data=ExamResult.objects.filter(institute=request.user.profile.institute, result_subject=subject,result_student_data=request.user, exam_sr_no=value)
                                for overall in overall_data:
                                    overall_subject=overall.result_subject
                                    
                                    if overall_subject==subject:
                                    
                                      overall_score=ExamResult.objects.filter(institute=request.user.profile.institute, result_student_data=request.user,exam_sr_no=value, result_subject=overall_subject)
                                      score_list=[]
                                      for overall in overall_score:
                                          score_list.append(overall.result_score)
                                      
                                      
                                      scored_data=list(score_list)
                                    
                                      score_list=list(map(int, scored_data))
                                      
                                      meanVal=statistics.mean(score_list)
                                      
                                      round_score=round(meanVal)
                                      
                            
    test_data=ExamResult.objects.filter(institute=request.user.profile.institute, result_student_data=request.user, result_score=round_score)
    for sub in test_data:
                  subject=sub.result_subject
                                        # print(subject)                                            
    for i in test_data:
                  i.marks=round_score
                                      
                                          
                                  
         
    context={
      
      'exam_sr_no':exam_sr_no,
      'exam_type_list':exam_type_list,
      "round_score":round_score,
      'test_data':test_data,
      'overall_data':overall_score

      }
    return render(request, 'overall.html', context)