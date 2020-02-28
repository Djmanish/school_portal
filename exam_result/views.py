from django.shortcuts import render
from .models import *
from main_app.models import *
from examschedule.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.db.models import Count




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
        #  print(exam_max_marks)
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
         for max_value in exam_result_data:
           
           marks_list.append(max_value.result_score)
         maxValue=marks_list[0]
         minValue=marks_list[0]
         sumVal=0
        #  sum_value=marks_list[0]         
         for i in range(0, len(marks_list),1):
          #  if maxValue<marks_list[i]:
              maxValue=max(maxValue, marks_list[i])
              minValue=min(maxValue, marks_list[i])
              # sumValue=sum(marks_list[i])
        #  print(maxValue)

         for j in range(0,len(marks_list), 1):
            minValue=min(minValue,marks_list[j])
        #  print(minValue)

        #  for n in range(len(marks_list)):
        #     sumValue=sum(sumVal, marks_list[n])
        #  print(sumValue)

        #  print(sumValue)
          #  for i in sum_score:
          #     sum_value=sum(sum_value,i)
             
             


         
        
          # score=(max_value.result_score)
          # max_score=score[0]
          # for i in range(0, len(score),1):
          #   if max_score < score[i]:
          #      max_score=score[i]
          # print(max_score)

          
        
        
         calculate_result=CalculateResult()
         calculate_result.institute=request.user.profile.institute
         calculate_result.calc_result_subject=selected_subject
         for data in exam_result_data:
          calculate_result.calc_result_score=data.result_score
         calculate_result.calc_result_max=maxValue
         calculate_result.calc_result_min=minValue
          

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
      examresult_data = ExamResult.objects.filter(institute=request.user.profile.institute,result_student_data=request.user, exam_type__exam_type= select_exam_type)
      exam_dataresult = ExamResult.objects.filter(institute=request.user.profile.institute, exam_type__exam_type= select_exam_type)
      exam_sr_no=ExamResult.objects.values('exam_sr_no').distinct()
      exam_data = ExamResult.objects.filter(institute=request.user.profile.institute, exam_type__exam_type= select_exam_type)
      max_marks=ExamType.objects.filter(institute=request.user.profile.institute, exam_type=select_exam_type)
      exam_subject = ExamResult.objects.filter(institute=request.user.profile.institute, exam_type__exam_type= select_exam_type)
      all_students_data=ExamResult.objects.filter(institute=request.user.profile.institute, exam_type__exam_type= select_exam_type )
    


      # get the value of exam serial number
     
      # for exam_no in exam_sr_no:
      #   result_sr_no=exam_no['exam_sr_no']
      #   for subjects in exam_dataresult:
      #       max_marks=[]
      #       exam_score = ExamResult(institute=request.user.profile.institute, result_subject=subjects.result_subject)
      #       for exam_score in exam_dataresult:
      #         # max_marks.append(exam_score)
      #         if exam_score.result_subject==subjects.result_subject:
                 
      #           max_marks.append(exam_score.result_score)
      #           marks=max(max_marks)
      #           print(marks)
      #           context ={
      #             'marks':marks,
      #           }
      #           return render(request, 'report_card.html', context)

                # context={
                #   'marks':marks,
                # }
                # return render(request, 'report_card.html', context)        

                # print(max(max_marks))


                # marks_list=list(max_marks)
                # print(max(max_marks))
                # value=max(max_marks)
                # print(value)
                

                #  print(exam_score.result_score)
          # exam_score=ExamResult.objects.filter(institute=request.user.profile.institute,exam_type__exam_type=select_exam_type, result_subject=subjects.result_subject, exam_sr_no=result_sr_no)
          
        #     print(subjects.result_subject)
        # print(result_sr_no)
          # print(subjects.result_score)
        
     
      # for exam_sr_no in exam_data:
      #   print(exam_sr_no.exam_sr_no)
      #   for student_subject in exam_subject:
      #     # student_subject_score=ExamResult.objects.filter(institute=request.user.profile.institute, result_subject=student_subject.result_subject)
        
      #     for student_score in exam_subject:
      #       student_subject_score=ExamResult.objects.filter(institute=request.user.profile.institute, result_subject=student_subject.result_subject)
      #       print(student_subject_score.result_score)


      #     print(student_subject.result_subject)
      #   print(exam_no)
    # subjects=Subjects.objects.filter(institute=request.user.profile.institute, subject_name=all_students_data.result_subject)
      # print(subjects.subject_name)
      # marks_list=[]
      # for data in all_students_data:
        # print(data.result_subject)
        
          # subject_marks=ExamResult.objects.filter(institute=request.user.profile.institute,result_subject=data.result_subject, exam_type__exam_type= select_exam_type)
          # print(subject_marks)
          # for marks in subject_marks:
          #     marks=marks.result_score
          #     marks_list.append(marks)
      # print(marks_list)


      context={
        'exam_type_list':exam_type_list,
        'examresult_data':examresult_data,
        'exam_sr_no':exam_sr_no,
        'select_exam_type':select_exam_type,
        'exam_subject':exam_subject,
        'all_students_data':all_students_data,
        'max_marks':max_marks,
              }
      return render(request, 'report_card.html', context)        
  context={
        'exam_type_list':exam_type_list,
        
        
      }

  return render(request, 'report_card.html', context)

