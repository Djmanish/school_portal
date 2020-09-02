from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from main_app.models import*
from .models import *
from django.contrib.auth.models import User

import datetime
from main_app.models import *
from Attendance import templates
from django.contrib import messages
from notices.models import *
from AddChild.models import *
from django.utils import timezone
from django.views import View
from django.core.exceptions import PermissionDenied
# import requests


#student detail
def student_detail(request,pk):
    # starting check if user has authorization to see list
    if  request.user.profile.designation.level_name == "principal" or request.user.profile.designation.level_name == "admin" or request.user.profile.designation.level_name == "teacher":
        pass
    else:
        raise PermissionDenied
    # starting check if user has authorization to see list
    # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
    student=UserProfile.objects.get(pk=pk, institute= request.user.profile.institute)
    context = {'student':student}
    return render (request, 'Attendance/student_detail.html', context)
    
# Create your views here.
def attendance(request):
    # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
    
    if request.method == "POST":
        students_class = Classes.objects.get(pk=request.POST.get('selected_class_attendance'))
        attendance_date = request.POST.get('attendance_date')
        current_date = str(datetime.date.today())

        if attendance_date > current_date:
            messages.error(request, "Attendance can't be taken for future dates !")
            return redirect('attendance')

        elif attendance_date < current_date:  # fetching record if attendance already taken
            attendance_record = Attendance.objects.filter(institute= request.user.profile.institute, student_class= students_class, date= attendance_date  )
            all_class = Classes.objects.filter(institute=request.user.profile.institute)
            context = {'all_students': attendance_record ,
                        'selected_class':all_class,
                        'selected_class_for_attendance':students_class,
                        'attendance_date': attendance_date}
            return render(request, 'Attendance/date_attendance_record.html', context)

        all_class = Classes.objects.filter(institute=request.user.profile.institute)
        designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='student')
        all_students= UserProfile.objects.filter(institute=request.user.profile.institute,designation= designation_pk, Class=students_class)

        # starting student statistics calculation
        session_start_date = request.user.profile.institute.session_start_date
        
        
        list_total_days_attendance_taken = []  #total days attendance taken for this session
        list_total_day_present = [] 
        list_total_day_absent = []
        list_total_day_leave = []

        for student in all_students:
            student = User.objects.get(pk = student.id)
            total_days_attendance_taken = Attendance.objects.filter(student= student, date__gte= session_start_date ).count()
            list_total_days_attendance_taken.append(total_days_attendance_taken)
        
        for student in all_students:
            student = User.objects.get(pk = student.id)
            total_days_present = Attendance.objects.filter(student= student, attendance_status="present", date__gte= session_start_date ).count()
            list_total_day_present.append(total_days_present)

        for student in all_students:
            student = User.objects.get(pk = student.id)
            total_day_absent = Attendance.objects.filter(student= student, attendance_status="absent", date__gte= session_start_date ).count()
            list_total_day_absent.append(total_day_absent)
        
        for student in all_students:
            student = User.objects.get(pk = student.id)
            total_day_leave = Attendance.objects.filter(student= student, attendance_status="leave", date__gte= session_start_date ).count()
            list_total_day_leave.append(total_day_leave)
        
        for (student, total_days, total_present, total_absent, total_leave) in zip(all_students, list_total_days_attendance_taken, list_total_day_present, list_total_day_absent, list_total_day_leave):
            student.total_days_taken_attendance = total_days
            student.total_present_count = total_present
            student.total_absent_count = total_absent
            student.total_leave_count = total_leave

        # ending student statistics calculation

      
        context = {'all_students': all_students,
         'selected_class':all_class,
         'selected_class_for_attendance':students_class,
         'attendance_date': attendance_date,
         'session_start_date':session_start_date}
         
        
        if students_class.class_teacher == request.user:
            return render(request, 'Attendance/Attendence.html', context)
        else:
            messages.error(request, "Only Class Teacher can mark attendance !")
            context = {
                'selected_class':all_class,
                 'selected_class_for_attendance':students_class,
            }
            return render(request, 'Attendance/Attendence.html', context )

    all_class = Classes.objects.filter(institute=request.user.profile.institute)  
    context = {'selected_class':all_class}
    return render(request, 'Attendance/Attendence.html', context,)

# def attendance_principal(request): 
#     return render(request, 'Attendance/attendance_principal.html',{'all_students': all_students})

def attendance_update(request, pk):
     
 student= User.objects.get(pk=pk) #student whose attendance marked
 student_institute = student.profile.institute
 student_class = student.profile.Class
 pk_str = str(pk) # pk of marked student
#  chk = Attendance.objects.all()
 if request.method == "POST":
        student_status = request.POST.get('pk_str') 
        attendance_date = request.POST.get('attendance_date')
        try:
            check_for_today = Attendance.objects.filter(student= student, date=attendance_date  )
            if len(check_for_today) !=0:
                return HttpResponse('<span style="color:red; padding:0px; margin:0px;">Taken already </span>')
            else:
                new_attendance = Attendance.objects.create(student=student,
                institute= student_institute,
                student_class = student_class,
                attendance_status=student_status, date=attendance_date )
                if student_status == "present":
                    return HttpResponse('<span style="color:green; padding:0px; margin:0px; font-weight:bolder">Present </span>')
                elif student_status == 'absent':
                    
                    # starting student absent notice
                    absent_notice = Notice()
                    absent_notice.institute = request.user.profile.institute
                    absent_notice.category='Attendance'
                    absent_notice.subject = f"{student.profile.first_name} {student.profile.last_name} Marked absent on {attendance_date}"
                    absent_notice.content = f"{student.profile.first_name} {student.profile.last_name} Marked absent on {attendance_date}"
                    absent_notice.created_at = timezone.now()
                    absent_notice.publish_date = timezone.now()
                    # absent_notice.author = request.user
                
                    absent_notice.save()
                    absent_student = UserProfile.objects.get(user= student)
                    student_parent = AddChild.objects.get(child= absent_student )
                
                    absent_notice.recipients_list.add(student_parent.parent)
                    absent_notice.recipients_list.add(absent_student)
                    


                    # ending student absent notice
                    return HttpResponse('<span style="color:red; padding:0px; margin:0px; font-weight:bolder">Absent </span>')
                else:
                    return HttpResponse('<span style="color:orange; padding:0px; margin:0px; font-weight:bolder">Leave </span>')
                
        except:
            pass
 return render(request, 'Attendance/Attendence.html')
        # return redirect('attendance')

def update_attendance_record(request, pk):
    
    # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
    student_to_update = User.objects.get(pk=pk)
    current_date = datetime.date.today()
    student_status = Attendance.objects.get(student = student_to_update, date = current_date)
    if request.method == 'POST':
        updated_status = request.POST.get('updated_status')
        student_status.attendance_status = updated_status
        student_status.save()

        all_class = Classes.objects.filter(institute=request.user.profile.institute)
        designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='student')
        all_students= UserProfile.objects.filter(institute=request.user.profile.institute,designation= designation_pk, Class=student_status.student_class)
        students_class = student_status.student_class
        attendance_date = current_date
        messages.success(request, "Attendace status updated successfully !")
        
        return redirect(f'/attendance/update_attendance_record/{pk}/')

    context = {
        'student_status': student_status
    }
    
    return render(request, 'Attendance/updating_attendance.html', context)


def current_date_attendance_record(request, pk):
    
    # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
    students_class = Classes.objects.get(pk=pk)
    attendance_record = Attendance.objects.filter(institute= request.user.profile.institute, student_class= students_class, date= datetime.date.today()  )
    session_start_date = request.user.profile.institute.session_start_date

    list_total_days_attendance_taken = []  #total days attendance taken for this session
    list_total_day_present = [] 
    list_total_day_absent = []
    list_total_day_leave = []

    for student in attendance_record:
        student_id = student.student.pk
        student = User.objects.get(pk = student_id)
        total_days_attendance_taken = Attendance.objects.filter(student= student, date__gte= session_start_date ).count()
        list_total_days_attendance_taken.append(total_days_attendance_taken)
        
    for student in attendance_record:
        
        student = User.objects.get(pk = student.student.id)
        total_days_present = Attendance.objects.filter(student= student, attendance_status="present", date__gte= session_start_date ).count()
        list_total_day_present.append(total_days_present)

    for student in attendance_record:
        student = User.objects.get(pk = student.student.id)
        total_day_absent = Attendance.objects.filter(student= student, attendance_status="absent", date__gte= session_start_date ).count()
        list_total_day_absent.append(total_day_absent)
        
    for student in attendance_record:
        student = User.objects.get(pk = student.student.id)
        total_day_leave = Attendance.objects.filter(student= student, attendance_status="leave", date__gte= session_start_date ).count()
        list_total_day_leave.append(total_day_leave)
        
    for (student, total_days, total_present, total_absent, total_leave) in zip(attendance_record, list_total_days_attendance_taken, list_total_day_present, list_total_day_absent, list_total_day_leave):
        student.total_days_taken_attendance = total_days
        student.total_present_count = total_present
        student.total_absent_count = total_absent
        student.total_leave_count = total_leave


  
    context = {'all_students': attendance_record ,
                       
                        'selected_class_for_attendance':students_class,
                        'attendance_date': datetime.date.today()}
    return render(request, 'Attendance/current_date_attendance_record.html', context)



def class_students_list(request):
    # starting check if user has authorization to see list
    if  request.user.profile.designation.level_name == "principal" or request.user.profile.designation.level_name == "admin" or request.user.profile.designation.level_name == "teacher":
        pass
    else:
        raise PermissionDenied
    # starting check if user has authorization to see list
    
    # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
    
    all_classes = Classes.objects.filter(institute= request.user.profile.institute)
    
    if request.method == "POST":
        selected_class = Classes.objects.get(pk = request.POST.get('selected_class_'))
        all_students = UserProfile.objects.filter(institute= request.user.profile.institute, Class= selected_class, designation__level_name='student', status="approve")
        if len(all_students)<1:
            messages.error(request, 'No student found in the selected class !')
            return redirect('class_students_list')
        

        context= {'all_students':all_students,
         'all_classes': all_classes,
         'showing_student_for_class':selected_class
         }
        return render(request, 'Attendance/class_students.html', context)
        
    context= {
        'all_classes': all_classes
    }
    return render(request, 'Attendance/class_students.html', context)


from .forms import Student_profile_edit_form, Student_info_edit_form


def student_detail_edit(request):
    user_profile = UserProfile.objects.get(pk= request.GET.get('username'), institute= request.user.profile.institute)
    # starting check if user has authorization to see list
    if  request.user.profile.designation.level_name == "principal" or request.user.profile.designation.level_name == "admin" or request.user.profile.designation.level_name == "teacher" and user_profile.Class in request.user.class_teacher.all() :
        pass
    else:
        raise PermissionDenied
    # starting check if user has authorization to see list
    # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
    
    # creating student info table instance for non existing student_details
    try:
        Student_Info.objects.get(student=user_profile)
        
    except:
        Student_Info.objects.create(student=user_profile)

    student_info_instace = Student_Info.objects.get(student=user_profile)

    student_prfile_edit_form = Student_profile_edit_form(instance= user_profile) # render form for userprofile model
    student_info_edit_form = Student_info_edit_form(instance=student_info_instace) # render for student info model

    if request.method == "POST":
        student_info = Student_info_edit_form(request.POST, request.FILES, instance=student_info_instace)
        student_details = Student_profile_edit_form(request.POST, request.FILES, instance=user_profile)#from userprofile form
         # from userinfo form
        
        if student_details.is_valid():
            messages.success(request, "Student's profile details updated successfully !")
            student_details.save()
            
        else:
            student_prfile_edit_form = Student_profile_edit_form(instance= user_profile)
            for field in student_details.fields: #code for sending form errors
                if student_details[field].errors:
                    for f in student_details[field].errors:
                        messages.error(request, f"{field} - {f}"  )
            messages.error(request, 'Details could not be updated !')
            return render(request, 'Attendance/edit_students_detail.html', {'student_prfile_edit_form':student_prfile_edit_form, 'student_info_edit_form':student_info_edit_form, 'student_details':student_details  })
            

        
        if student_info.is_valid():
            student_info.save()
            messages.success(request, "Student's additional information updated successfully !")
            return HttpResponseRedirect(f"/attendance/student_detail/{request.GET.get('username')}/")
            
        else:
            for field in student_info.fields: #code for sending form errors
                if student_info[field].errors:
                    for f in student_info[field].errors:
                         messages.error(request, f"{field} - {f}"  )
            student_info_edit_form = Student_info_edit_form(instance=student_info_instace)
            messages.error(request, 'Details could not be updated !')
            
    context = {

            'student_prfile_edit_form':student_prfile_edit_form,
            'student_info_edit_form':student_info_edit_form,
            'user_profile':user_profile
        }

    return render(request, 'Attendance/edit_students_detail.html', context)
