from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from main_app.models import*
from .models import *
from django.contrib import messages
from Attendance.models import *
from exam_result.models import *
from examschedule.models import *
from main_app.views import *
# Create your views here.
def addchild(request):
    institutes=Institute.objects.all()
    
    
    if request.method == "POST":
        selected_institute= Institute.objects.get(pk=request.POST.get("selected_institute"))
        selected_class = Classes.objects.get(pk=request.POST.get('selected_class'))
        roll_number=request.POST.get('roll_number')
        try:
            student = UserProfile.objects.get(institute=selected_institute,Class=selected_class,roll_number=roll_number)
        except UserProfile.DoesNotExist:
            # messages.success(request, 'Requested Child Not Found')
            student=None
        
        child_search= None
        # start chk for student already listed or not
        if student != None:
            try:
                child_search = AddChild.objects.get(child=student)
                if child_search.parent == request.user.profile:
                    messages.info(request,'Already added in your list !')
                else:
                    messages.info(request, 'Requested Child already associated with some other parent !')
            except AddChild.DoesNotExist:
                child_search=None
        
        # starting checking if already selected as child
        try:
            parent_child_check = AddChild.objects.filter(parent= request.user.profile, child = student)
            
            if len(parent_child_check) > 0 :
                    student.is_already_listed = True
            else:
                student.is_already_listed = False
        except:
            pass   
            
        # ending checking if already selected as child
        context = {
            'institutes':institutes,
            'student':student,
            'child_search':child_search,
            }
        return render(request, 'AddChild/child.html', context)

    context = {
            'institutes':institutes,
          

    }    
        
    return render(request, 'AddChild/child.html', context)
def fetch_institute_class(request):
    selected_school  = Institute.objects.get(pk=request.POST.get('school_id'))
    schools_all_classes = Classes.objects.filter(institute= selected_school)
    classes = ""
    for Class in schools_all_classes:
        classes= classes+ f"<option value='{Class.id}' >"+str(Class)+"</option>"
    return HttpResponse(classes)

def addchildtolist(request,pk):
    student_tolist =pk
    student1= UserProfile.objects.get(id=pk)
    parent=request.user.profile
    add_child = AddChild.objects.create(parent=parent, child=student1, institute=student1.institute, Class=student1.Class)
    messages.success(request, 'Request has been sent for the selected child !')
    return redirect('user_profile')

def approve_child_request(request,pk):
    

    user = AddChild.objects.get(pk=pk)
    user.approve()
    rr= request.user.profile.institute.id
    return HttpResponseRedirect(f'/user/approvals/{rr}/')

def disapprove_child_request(request,pk):
    user = AddChild.objects.get(pk=pk)
    user.delete()
    rr= request.user.profile.institute.id
    return HttpResponseRedirect(f'/user/approvals/{rr}/')

def delete_child_request(request,pk):
    user = AddChild.objects.get(pk=pk)
    user.delete()
    rr= request.user.profile.institute.id
    return HttpResponseRedirect('/user/dashboard/')

def childview(request,pk):
    
    child = AddChild.objects.get(parent=request.user.profile,pk=pk)
    child_subjects=Subjects.objects.filter(institute=child.child.institute,subject_class=child.child.Class)
    child_user=User.objects.get(username=child.child)
    child_total_attendance=Attendance.objects.filter(student=child_user,institute=child.child.institute,student_class=child.child.Class).count()
    child_total_present=Attendance.objects.filter(student=child_user,institute=child.child.institute,student_class=child.child.Class,attendance_status="present").count()
    child_total_absent=Attendance.objects.filter(student=child_user,institute=child.child.institute,student_class=child.child.Class,attendance_status="absent").count()
    try:
        present=(child_total_present/child_total_attendance)*100
        absent=(child_total_absent/child_total_attendance)*100
    except ZeroDivisionError:
        present=0
        absent=0
    # exam_t=ExamType.objects.filter(institute=request.user.profile.institute)
    # try:
    #     exam_type_child=ExamType.objects.filter(institute=request.user.profile.institute).latest('id')
    # except ExamType.DoesNotExist:
    #     pass
    # max_marks=exam_type_child.exam_max_marks
    # total_marks=Subjects.objects.filter(institute=child.child.institute,subject_class=child.child.Class).count()*int(max_marks)
    # child_result=ExamResult.objects.filter(exam_type=exam_type_child,result_student_data=child_user)
    # total_sum = 0
    # for i in child_result:
    #     i = i.result_score
    #     total_sum = total_sum + int(i)
    # m=int(total_marks)
    # try:
    #     avg=((total_sum/m)*100)
    # except ZeroDivisionError:
    #     avg=0
    
    # if (avg<33):
    #     result="Fail"
    # else:
    #     result="Pass"
    # For events & Calendars
    child_she=ExamDetails.objects.filter(institute=child.child.institute,exam_class=child.child.Class)
    
    if request.method == "POST":
        child = AddChild.objects.get(parent=request.user.profile,pk=pk)
        child_subjects=Subjects.objects.filter(institute=child.child.institute,subject_class=child.child.Class)
        child_user=User.objects.get(username=child.child)
        child_total_attendance=Attendance.objects.filter(student=child_user,institute=child.child.institute,student_class=child.child.Class).count()
        child_total_present=Attendance.objects.filter(student=child_user,institute=child.child.institute,student_class=child.child.Class,attendance_status="present").count()
        child_total_absent=Attendance.objects.filter(student=child_user,institute=child.child.institute,student_class=child.child.Class,attendance_status="absent").count()
        try:
            present=(child_total_present/child_total_attendance)*100
            absent=(child_total_absent/child_total_attendance)*100
        except ZeroDivisionError:
            present=0
            absent=0
        
        examty=request.POST.get("selected_exam_type")
        print(examty)
        ty=ExamType.objects.get(id=examty)
        exam_type_child=ExamType.objects.filter(institute=request.user.profile.institute).latest('id')
        max_marks=exam_type_child.exam_max_marks
        total_marks=Subjects.objects.filter(institute=child.child.institute,subject_class=child.child.Class).count()*int(max_marks)
        child_result_p=ExamResult.objects.filter(exam_type=examty,result_student_data=child_user)        
        total_sum = 0
        for i in child_result_p:
            i = i.result_score
            total_sum = total_sum + int(i)
        m=int(total_marks)
        avg=(total_sum/m)*100
        if (avg<33):
            result="Fail"
        else:
            result="Pass"

        child_she=ExamDetails.objects.filter(institute=child.child.institute,exam_class=child.child.Class)
        
        context={
            'ty':ty,
            'child_result_p':child_result_p,
            # 'exam_t':exam_t,
        # 'exam_type_child':exam_type_child,
        'present':present,
        'absent':absent,
        'child_subjects':child_subjects,
        'child':child,
        # 'result':result,
        'child_she':child_she,
        }
        return render(request, 'AddChild/viewchild.html',context)
    context={
        # 'exam_t':exam_t,
        # 'exam_type_child':exam_type_child,
        # 'child_result':child_result,
        'present':present,
        'absent':absent,
        'child_subjects':child_subjects,
        'child':child,
        # 'result':result,
        'child_she':child_she
    }
    return render(request, 'AddChild/viewchild.html',context)

def secondry_institute(request):
    institutes=Institute.objects.all()
    
    
    if request.method == "POST":
        selected_institute= Institute.objects.get(pk=request.POST.get("selected_institute"))
        selected_class = Classes.objects.get(pk=request.POST.get('selected_class'))
        roll_number=request.POST.get('roll_number')
        add_child = SecondryInstitute.objects.create(student_name=request.user.profile, student_institute=selected_institute, student_Class=selected_class,student_rollno=roll_number)
        messages.success(request, 'Request has sent to add Institute !')
        return redirect('user_profile')
        # student = UserProfile.objects.get(institute=selected_institute,Class=selected_class,roll_number=roll_number)
        
        # starting checking if already selected as child
        # parent_child_check = AddChild.objects.filter(parent= request.user.profile, child = student)
        # if len(parent_child_check) > 0 :
        #     student.is_already_listed = True
        # else:
        #     student.is_already_listed = False
            
        # ending checking if already selected as child
        

    context = {
            'institutes':institutes,
          

    }    
        
    return render(request, 'AddChild/secondry.html', context)
