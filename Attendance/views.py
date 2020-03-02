from django.shortcuts import render, HttpResponse, redirect
from main_app.models import*
from .models import *
from django.contrib.auth.models import User

import datetime
from main_app.models import *
from Attendance import templates
from django.contrib import messages
# import requests

# Create your views here.
def attendance(request):
    if request.method == "POST":
        students_class = Classes.objects.get(pk=request.POST.get('selected_class_attendance'))
        attendance_date = request.POST.get('attendance_date')
        current_date = str(datetime.date.today())

        if attendance_date > current_date:
            messages.error(request, "Attendance can't be taken for future dates")
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
            messages.error(request, "Only Class Teacher can mark attendance")
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
                    return HttpResponse(f'<span style="color:green; padding:0px; margin:0px; font-weight:bolder">{student_status} </span>')
                elif student_status == 'absent':
                    return HttpResponse(f'<span style="color:red; padding:0px; margin:0px; font-weight:bolder">{student_status} </span>')
                else:
                    return HttpResponse(f'<span style="color:orange; padding:0px; margin:0px; font-weight:bolder">{student_status} </span>')
                
        except:
            pass
 return render(request, 'Attendance/Attendence.html')
        # return redirect('attendance')

def update_attendance_record(request, pk):
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
        messages.success(request, "Attendace status updated successfully")
        
        return redirect(f'/attendance/update_attendance_record/{pk}/')

    context = {
        'student_status': student_status
    }
    
    return render(request, 'Attendance/updating_attendance.html', context)


def current_date_attendance_record(request, pk):
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
    all_classes = Classes.objects.filter(institute= request.user.profile.institute)
    
    if request.method == "POST":
        selected_class = Classes.objects.get(pk = request.POST.get('selected_class_'))
        all_students = UserProfile.objects.filter(institute= request.user.profile.institute, Class= selected_class, designation__level_name='student')
        if len(all_students)<1:
            messages.error(request, 'No student found in the selected class')
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

    