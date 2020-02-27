from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from main_app.models import *
from .models import *
from django.contrib import messages

# Create your views here.


def admission_home(request):
    school_list = Institute.objects.all()
    states_list = State.objects.all()
    context = {
        'school_list': school_list,
        'states_list': states_list
    }
    if request.method == "POST":
        new_request = Admission_Query()
        new_request.first_name= request.POST.get('first_name')
        new_request.middle_name= request.POST.get('middle_name')
        new_request.last_name = request.POST.get('last_name')
        new_request.father_name = request.POST.get('father_name')
        new_request.mother_name = request.POST.get('mother_name')
        new_request.date_of_birth = request.POST.get('date_of_birth')
        new_request.gender = request.POST.get('gender')
        new_request.Category = request.POST.get('category')
        new_request.school_name = Institute.objects.get(pk= request.POST.get('school'))
        new_request.class_name = Classes.objects.get(pk=request.POST.get('class'))
        new_request.mobile_Number = request.POST.get('mobile_number')
        new_request.Email_Id = request.POST.get('email')
        new_request.Nationality = request.POST.get('nationality')
        new_request.Address= request.POST.get('address')
        new_request.District = request.POST.get('district')
        new_request.State = State.objects.get(pk=request.POST.get('state'))
        new_request.Pin_Code = request.POST.get('pin_code')
        new_request.Student_Photo= request.FILES['student_pic']
        try:
            new_request.save()
            messages.success(request, 'We have received your data. We will get back to you soon.')
            return redirect('admission_home')
        except:
            messages.error(request, 'failed to submit, Please fill all details carefully')
            return redirect('admission_home')

            
    
    context = {
        'school_list': school_list,
        'states_list': states_list
    }
    return render( request , 'admissions/admission_home.html', context)

def fetch_institute_class_admission(request):
    selected_school  = Institute.objects.get(pk=request.POST.get('school_id'))
    schools_all_classes = Classes.objects.filter(institute= selected_school)
    classes = "<option selected disabled value="">-- select Clas -- </option>"
    for Class in schools_all_classes:
        classes= classes+ f"<option value='{Class.id}' >"+str(Class)+"</option>"
    return HttpResponse(classes)
    
