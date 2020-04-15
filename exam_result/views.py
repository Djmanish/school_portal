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

# Create your views here.
def exam_result(request,pk):
      result_institute=Institute.objects.get(pk=pk)
      exam_result_institute=ExamResult.objects.filter(institute=result_institute)
      #  to fetch the logged in  subject teacher
      subject_result=Subjects.objects.filter(institute=request.user.profile.institute, subject_teacher=request.user)
      institute_exam_type=ExamType.objects.filter(institute=request.user.profile.institute)


    # -----------------------------------------------------------------------------------

      if request.method=="POST":
        selected_subject = Subjects.objects.get(pk=request.POST.get('result_selected_subject'))
        result_exam_type=request.POST.get('result_exam_type')
        if result_exam_type==None:
                    etype=ExamType.objects.get(institute= request.user.profile.institute, exam_type=result_exam_type)
                    exam_type=etype.id
                    result_exam_type=exam_type
        exam_type_id=ExamType.objects.get(exam_type=result_exam_type)
        result_exam_type_sr_no = request.POST.get('fetch_sr_no')
        

      #============================================================================================ 
        student_designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='student')
        institute_students = UserProfile.objects.filter(institute= request.user.profile.institute, designation=student_designation_pk,Class=selected_subject.subject_class)
        
        

        context={
                  'subject_result':subject_result,
                  
                  'selected_subject':selected_subject,
                  'exam_type_id':exam_type_id,
                  'result_exam_type_sr_no':result_exam_type_sr_no,
                  'institute_exam_type':institute_exam_type,
                  'institute_students':institute_students,
                  
                  }
        return render(request, 'teacher_view.html', context) 
    # ----------------------------------------------------------------------------------------------
  
      context={
                  'subject_result':subject_result,
                  'institute_exam_type':institute_exam_type,
                  
                 
                  }
                
      return render(request, 'teacher_view.html', context)    


    
def examresult(request,pk):
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
          
                data_list=list(marks_list)
                marks_list=list(map(int, data_list))
                check_limit=int(exam_max_marks)
          for score in marks_list:
                  
                  if score<check_limit or score==check_limit:

                              pass
                  
                  else:
                              messages.info(request, 'Not Approriate Marks')
                              return redirect('not_found')
              
                
          for subject in exam_result_data:
                        subject=subject.result_subject
                        
                        meanVal=statistics.mean(marks_list)

                        maxValue=max(data_list)
                        minValue=min(data_list)
                        avgValue=round(meanVal)
                        sumValue=sum(marks_list)
          print(maxValue)
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
  
  max_exam_sr_no = ExamDetails.objects.filter(exam_type__exam_type=exam_type_id).values('exam_sr_no').distinct()
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
# get Exam Type
  exam_type_list =ExamType.objects.filter(institute=request.user.profile.institute)
  exam_id=request.user.profile.institute.id

  if request.method=="POST":
      select_exam_type = request.POST.get('result_exam_type')
      
      if select_exam_type=="Overall":
         return HttpResponseRedirect(f'/examresult/overall_result/{exam_id}/')
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
      
      if score_list:
                    pass
      else:
                    messages.info(request, 'It seems there are no Exam Result of this Exam Type in the institute.')
                    return redirect('not_found')

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
   
    sr_no=ExamDetails.objects.filter(institute=request.user.profile.institute)
    exam_type_list=ExamType.objects.filter(institute=request.user.profile.institute)
    exam_sr_no=ExamResult.objects.values('exam_sr_no').distinct()
    for sr_no in exam_sr_no:
                for key,value in sr_no.items():
                                  result_type=ExamResult.objects.filter(institute=request.user.profile.institute)
                                  for rtype in result_type:
                                      r_type=rtype.exam_type
                                      exam_subjects=ExamResult.objects.filter(institute=request.user.profile.institute, result_student_data=request.user, exam_type=r_type)
                                                      
                                      for exam_sub in exam_subjects:
                                        subject=exam_sub.result_subject
                            
                                      
                                        overall_data=ExamResult.objects.filter(institute=request.user.profile.institute,result_student_data=request.user,exam_type__exam_type=r_type, exam_sr_no=value)
                                        for overall in overall_data:
                                            overall_subject=overall.result_subject
                                           
                                            if overall_subject==subject:
                                              overall_score=ExamResult.objects.filter(institute=request.user.profile.institute, result_student_data=request.user,exam_sr_no=value, result_subject=overall_subject)
                                              score_list=[]
                                              for overall in overall_score:
                                                  score_list.append(overall.result_score)
                                              
                                              scored_data=list(score_list)
                                              
                                              score_list=list(map(int, scored_data))
                                              sum_score_list=sum(score_list)
                                              
                                              meanVal=statistics.mean(score_list)
                                              round_score=round(meanVal)
                                              
                                              
                                              test_data=ExamResult.objects.filter(institute=request.user.profile.institute, result_student_data=request.user,  exam_type=r_type,exam_sr_no=value)
                                              for subject_marks in test_data:
                                                    subject_marks.marks=round_score
                                                    
                                                   
                                              
                    
                                              context={
                                                'test_data':test_data,
                                                'exam_type_list':exam_type_list,
                                                 
                                                 'overall_subject':overall_subject,
                                              } 
                                              return render(request, 'overall.html', context)                         
                                                  
                                  
        
    context={
      
      'sr_no':sr_no,
      'exam_type_list':exam_type_list,
      }
    return render(request, 'overall.html', context)
  
  
def class_promotion(request,pk):

    
    current_year=datetime.date.today().year
    next_year=datetime.date.today().year+1
    
    # to get the list of all  classes                                        
    all_classes = Classes.objects.filter(institute= request.user.profile.institute)

    # to ge the data through POST method
    if request.method=="POST":
        selected_class =Classes.objects.get(pk=request.POST.get('selected_class_promotion'))
     
            
            
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
                              user_d.Class=promoted_to_class
                              user_d.class_current_year=current_year+1
                              user_d.class_next_year=next_year+1

                              user_d.save()
           # Inner Context
        context= {
            'all_classes': all_classes,
            'all_students':all_students,
            'list_promotion_choices':list_promotion_choices,
        }
        return render(request, 'class_promotion.html', context)


                          
    # Outer Context
    context= {
        'all_classes': all_classes,
        
    }
    return render(request, 'class_promotion.html', context)



def st_result(request):
  pass
