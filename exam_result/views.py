from django.shortcuts import render
from .models import *
from main_app.models import *
from examschedule.models import *
from django.http import HttpResponseRedirect, HttpResponse



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
  # result_exam_type=request.GET.get('result_exam_type')
  # if result_exam_type==None:
  #     result_type=ExamType.objects.filter(institute=request.user.profile.institute).last()
  #     result_type_id=result_type.id
  #     result_exam_type=result_type_id
  # selected_exam_type=ExamType.objects.get(pk=result_exam_type)
  # print(selected_exam_type)
  # to fetch the institute students based on selected class 
  student_designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='student')
  institute_students = UserProfile.objects.filter(institute= request.user.profile.institute, designation=student_designation_pk,Class=selected_subject.subject_class)
  # to store the value of Exam Type
  
 # to get the data from the individual row
  if request.method=="POST":
    
           
      # select_exam_type = request.POST.get('result_exam_type')
      
      # select_exam_type_no = request.POST.get('fetch_result_sr_no')
      selected_exam_tyep =  ExamType.objects.filter(institute= request.user.profile.institute, exam_type= result_exam_type).first()
      for sdata,score in zip(request.POST.getlist('student_first_name'),request.POST.getlist('student_marks')):

         sdata = UserProfile.objects.get(pk=sdata)
         exam_max_marks=request.POST.get('exam_max_marks')
         marks_data=ExamResult()
         marks_data.institute=request.user.profile.institute
         marks_data.exam_sr_no= result_exam_type_sr_no
         marks_data.exam_type= selected_exam_tyep
         marks_data.result_class=selected_subject.subject_class
         marks_data.result_subject=selected_subject
         marks_data.result_subject_teacher=selected_subject.subject_teacher
         marks_data.result_student_data=sdata
         marks_data.result_max_marks=exam_max_marks
         marks_data.result_score=score
         marks_data.save()
      # messages.success(request, 'Exam Result Stored successfully !!!')
 




  context={
    'subject_result':subject_result,
    'selected_subject':selected_subject,
    'institute_students':institute_students,
    # 'result_exam_type':result_exam_type,
    # 'result_exam_code':result_exam_code,
    'institute_exam_type':institute_exam_type,
   
  }
  return render(request, 'teacher_view.html', context)

#  Principal View
def exam_view(request,pk):

    exam_details=ExamType.objects.all()
    if request.method=="POST":
      for  per_score, exam_type in zip(request.POST.getlist('per_score'),request.POST.getlist('examview_examtype')): 
        exam_type_id=ExamType.objects.get(pk=exam_type)
        
        examview=ExamView()
        
        examview.exam_percent_score=per_score
        examview.pexamview_type=ExamType.objects.get(pk=exam_type)
        examview.save()
    context={
    'exam_details':exam_details,
           }
    return render(request, 'principal_view.html', context)


    # Student View

def student_view(request,pk):
    student_view=ExamResult.objects.all()
   
    

    context={
      'student_view':student_view,
    }
    return render(request, 'studentview.html' , context)


def fetch_sr_no(request):
  exam_type_id = request.POST.get('exam_type_id')
  
  max_exam_sr_no = ExamDetails.objects.filter(exam_type__exam_type=exam_type_id).values('exam_sr_no').distinct()
  individual_result_sr_no = ""
  for result_sr_no in max_exam_sr_no:
    individual_result_sr_no = individual_result_sr_no + f"<option >"+result_sr_no['exam_sr_no']+"</option>"  
  return HttpResponse(individual_result_sr_no)