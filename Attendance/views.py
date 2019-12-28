from django.shortcuts import render
from main_app import views
from main_app import templates
from main_app.models import *
from Attendance import templates

# Create your views here.
def attendance(request):
    designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='student')
    all_students= UserProfile.objects.filter(institute=request.user.profile.institute, designation= designation_pk)
    return render(request, 'Attendance/Attendence.html',{'all_students': all_students})