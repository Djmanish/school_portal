from django.shortcuts import render, HttpResponse, redirect
from main_app.models import*
from .models import *
from django.contrib.auth.models import User


from main_app.models import *
from Attendance import templates

# Create your views here.
def attendance(request):

    designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='student')
    
    all_students= UserProfile.objects.filter(institute=request.user.profile.institute, designation= designation_pk)
    
    return render(request, 'Attendance/Attendence.html',{'all_students': all_students})

def attendance_update(request, pk):
    
    student= User.objects.get(pk=pk) #student whose attendance marked
    pk_str = str(pk) # pk of marked student
    if request.method == "POST":
        student_status = request.POST.get('pk_str')
        
        new_attendance = Attendance.objects.create(student=student, attendance_status=student_status)
        return HttpResponse(f'{pk}')
        # return redirect('attendance')


