from django.shortcuts import render, HttpResponse, redirect
from main_app.models import*
from .models import *
from django.contrib.auth.models import User

import datetime
from main_app.models import *
from Attendance import templates
from django.contrib import messages

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

        context = {'all_students': all_students,
         'selected_class':all_class,
         'selected_class_for_attendance':students_class,
         'attendance_date': attendance_date}
        
        
        return render(request, 'Attendance/Attendence.html', context)

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
                return HttpResponse('<p style="color:red;">Attendance Already Taken for this Date !!!</p>')
            else:
                new_attendance = Attendance.objects.create(student=student,
                institute= student_institute,
                student_class = student_class,
                 attendance_status=student_status, date=attendance_date )
            return HttpResponse(f'<p style="color:green;">Attendance Submitted as {student_status} </p>') 
        except:
            pass
            
        
 return render(request, 'Attendance/Attendence.html')
        # return redirect('attendance')
