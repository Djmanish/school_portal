from django.shortcuts import render
from .models import *
from main_app.models import *


# Create your views here.
def exam_result(request,pk):
  # to fetch the current institute
  result_institute=Institute.objects.get(pk=pk)
  exam_result_institute=ExamResult.objects.filter(institute=result_institute)
  
  #  to fetch the logged in  subject teacher
  subject_result=Subjects.objects.filter(institute=request.user.profile.institute, subject_teacher=request.user)
  
 # to fetch the value of selected subject
  result_subject=request.GET.get('result_selected_subject')
  if result_subject== None:
       first_subject=Subjects.objects.filter(institute= request.user.profile.institute).last()
       first_subject_id=first_subject.id
       result_subject=first_subject_id
  selected_subject= Subjects.objects.get(pk=result_subject)
  
  # to fetch exam type objects
  result_max_marks=request.GET.get('result_selected_exam_type')
  if result_max_marks==None:
     max_marks=ExamType.objects.filter(institute=request.user.profile.institute).last()
     max_marks_id=max_marks.id
     result_max_marks=max_marks_id
  selected_max_marks=ExamType.objects.get(pk=result_max_marks)

  
  # to fetch the institute students based on selected class 
  student_designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='student')
  institute_students = UserProfile.objects.filter(institute= request.user.profile.institute, designation=student_designation_pk,Class=selected_subject.subject_class)
  
  # to store the value of Exam Type

  result_exam_type = ExamType.objects.filter(institute=request.user.profile.institute)

 # to get the data from the individual row
  if request.method=="POST":
           
     for sdata,score in zip(request.POST.getlist('student_first_name'),request.POST.getlist('student_marks')):

         result_subject=request.GET.get('result_selected_subject')
         result_exam_type_id=ExamType.objects.get(pk=request.GET.get('result_selected_exam_type'))
         sdata = UserProfile.objects.get(pk=sdata)
         result_examtype_marks=ExamType.objects.filter(exam_type=result_exam_type_id)

         
         marks_data=ExamResult()
         marks_data.institute=request.user.profile.institute
         marks_data.result_class=selected_subject.subject_class
         marks_data.result_subject=Subjects.objects.get(pk=result_subject)
         marks_data.result_subject_teacher=selected_subject.subject_teacher
         marks_data.result_exam_type=result_exam_type_id
         marks_data.result_student_data=sdata
         marks_data.result_max_marks=selected_max_marks.exam_max_marks
         marks_data.result_score=score
         marks_data.save()
  # messages.success(request, 'Exam Result Stored successfully !!!')





  context={
    'subject_result':subject_result,
    'selected_subject':selected_subject,
    'institute_students':institute_students,
    'result_exam_type':result_exam_type,
   
  }
  return render(request, 'teacher_view.html', context)


def exam_view(request,pk):
    institute=Institute.objects.get(pk=pk)
    exam_type=ExamType.objects.filter(institute=request.user.profile.institute)
    exam_type_subject=request.GET.get('examview_type')
    if exam_type_subject==None:
        max_marks=ExamResult.objects.filter(institute=request.user.profile.institute).last()
        max_marks_id=max_marks.id
        exam_type_subject=max_marks_id
    # selected_exam_type=ExamType.objects.get(pk=exam_type_subject)
    # examresult_data=ExamResult.objects.filter(result_exam_type=selected_exam_type)
    

    
    if request.method=="POST":
       examresult_data=ExamResult.objects.filter(institute=request.user.profile.institute)
       
       examview=ExamView()
       examview.examview_type=selected_exam_type
       examview.examview_subject=examresult_data.result_subject
       examview.save()
    context={
    
      'exam_type':exam_type,
      
      # 'examresult_data':examresult_data,

    }
    return render(request, 'principal_view.html', context)