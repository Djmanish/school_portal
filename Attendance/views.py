from django.shortcuts import render, HttpResponse, redirect
from main_app.models import*
from .models import *
from django.contrib.auth.models import User


from main_app.models import *
from Attendance import templates

# Create your views here.
def attendance(request):
    if request.method == "POST":
        students_class = Classes.objects.get(pk=request.POST.get('selected_class_attendance'))
        all_class = Classes.objects.filter(institute=request.user.profile.institute)
        designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='student')
        all_students= UserProfile.objects.filter(institute=request.user.profile.institute,designation= designation_pk, Class=students_class)
        chk=Attendance.objects.all()
        
        return render(request, 'Attendance/Attendence.html',{'all_students': all_students, 'selected_class':all_class},{'chk':chk})

    all_class = Classes.objects.filter(institute=request.user.profile.institute)  
    return render(request, 'Attendance/Attendence.html',{'selected_class':all_class})

# def attendance_principal(request): 
#     return render(request, 'Attendance/attendance_principal.html',{'all_students': all_students})

def attendance_update(request, pk):
     
 student= User.objects.get(pk=pk) #student whose attendance marked
 current_date = datetime.date.today() 
 pk_str = str(pk) # pk of marked student
#  chk = Attendance.objects.all()


   
 if request.method == "POST":
        student_status = request.POST.get('pk_str') 
        try:
            check_for_today = Attendance.objects.filter(student= student, date=current_date  )
            if len(check_for_today) !=0:
                return HttpResponse('attendance taken for today')
            else:
                new_attendance = Attendance.objects.create(student=student, attendance_status=student_status, date=current_date )
            return HttpResponse('Attendance Submitted') 
        except:
            pass
            
        
 return render(request, 'Attendance/Attendence.html')
        # return redirect('attendance')
