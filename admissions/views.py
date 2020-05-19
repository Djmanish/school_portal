from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from main_app.models import *
from .models import *
from django.contrib import messages
from django.views.generic import ListView, DetailView
from PIL import Image
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from notices.models import *
from django.utils import timezone

# Create your views here.


def admission_home(request):
    try:
        if_already_user = Role_Description.objects.get(user=request.user)
        messages.info(request, 'You are not allowed to visit this page !')
        return redirect('not_found')
    except:
        pass

    try:
        if_already_requested = Admission_Query.objects.get(request_by= request.user)
        if if_already_requested:
            messages.info(request, 'You have already requested. Please wait till any response from your school !')
            school_list = Institute.objects.all()
            states_list = State.objects.all()
            context = {
                'school_list': school_list,
                'states_list': states_list,
                'disable_submit':'disabled'
            }
            return render( request , 'admissions/admission_home.html', context)        
    except:
        pass
    
    school_list = Institute.objects.all()
    states_list = State.objects.all()
    context = {
        'school_list': school_list,
        'states_list': states_list
    }
    if request.method == "POST":
        # starting code for checking profile pic extension
        Student_Photo= request.FILES['student_pic']
        fname = Student_Photo.name
        if  fname.endswith('.jpeg') or fname.endswith('.jpg') or fname.endswith('.gif'):
            pass
        else:
            messages.error(request, 'invalid photo format. Only jpeg, jpg format are allowed !')
            return redirect('admission_home')
        #  ending code for checking profile pic extension



        new_request = Admission_Query()
        new_request.first_name= request.POST.get('first_name').strip()
        new_request.middle_name= request.POST.get('middle_name').strip()
        new_request.last_name = request.POST.get('last_name').strip()
        new_request.father_name = request.POST.get('father_name').strip()
        new_request.mother_name = request.POST.get('mother_name').strip()
        new_request.date_of_birth = request.POST.get('date_of_birth')
        new_request.gender = request.POST.get('gender')
        new_request.Category = request.POST.get('category')
        new_request.school_name = Institute.objects.get(pk= request.POST.get('school'))
        new_request.class_name = Classes.objects.get(pk=request.POST.get('class'))
        new_request.mobile_Number = request.POST.get('mobile_number')
        new_request.Email_Id = request.POST.get('email')
        new_request.Nationality = request.POST.get('nationality')
        new_request.Address= request.POST.get('address').strip()
        new_request.District = request.POST.get('district').strip()
        new_request.State = State.objects.get(pk=request.POST.get('state'))
        new_request.Pin_Code = request.POST.get('pin_code')
        new_request.Student_Photo= request.FILES['student_pic']
        new_request.request_by = request.user
        try:
            new_request.save()
            messages.success(request, 'We have received your data. We will get back to you soon !')
            return redirect('user_dashboard')
        except:
            messages.error(request, 'Failed to submit, Please fill all details carefully !')
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
    

class Admission_Requests_View(LoginRequiredMixin, UserPassesTestMixin,  ListView ):
    model = Admission_Query
    template_name = "admissions/admission_requests.html"
    paginate_by = 20

    def test_func(self):
        if self.request.user.profile.designation.level_name == "admin" or self.request.user.profile.designation.level_name == "principal":
            return True
        else:
            return False
    
    
    def get_context_data(self, **kwargs):
            
    # starting user notice
        if self.request.user.profile.designation:
            self.request.user.users_notice = Notice.objects.filter(institute=self.request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = self.request.user.profile).order_by('id').reverse()[:10]
        # ending user notice
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        return context

    
    def get_queryset(self):
        return Admission_Query.objects.filter(school_name= self.request.user.profile.institute)

class Admission_Request_Detail_View(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model= Admission_Query
    template_name = "admissions/admission_request_detail_view.html"
    def test_func(self):
        if self.request.user.profile.designation.level_name == "admin" or self.request.user.profile.designation.level_name == "principal":
            return True
        else:
            return False

    
    def get_context_data(self, **kwargs):
            
    # starting user notice
        if self.request.user.profile.designation:
            self.request.user.users_notice = Notice.objects.filter(institute=self.request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = self.request.user.profile).order_by('id').reverse()[:10]
        # ending user notice
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        return context



def fetching_disapproved_id(request, pk):
    admission_request = Admission_Query.objects.get(pk=pk)
    
    data = {'name':admission_request.first_name, 'id':admission_request.id}
    return HttpResponse(f"Are you sure to disapprove {admission_request.first_name}")

def disapprove_admission_request(request, pk):
    to_delete = Admission_Query.objects.get(pk=pk)
    to_delete.delete()
    return redirect('admission_requests')


def approve_admission_request(request, pk):
    approved_user = Admission_Query.objects.get(pk=pk)
    approved_user_class = approved_user.class_name
    approved_user_first_name = approved_user.first_name
    
    
    approved_user = approved_user.request_by
    student_designation = Institute_levels.objects.get(institute= request.user.profile.institute, level_name='student')
    
    approved_user_profile = UserProfile.objects.get(user= approved_user)
    approved_user_profile.designation = student_designation
    approved_user_profile.institute = request.user.profile.institute
    approved_user_profile.Class = approved_user_class
    approved_user_profile.status= 'approve'
    approved_user_profile.first_name = approved_user_first_name
    
    
    try:
        Role_Description.objects.create(user=approved_user, institute= request.user.profile.institute, level=student_designation)       
    except:
        messages.info(request, 'user already exists')
        return redirect('user_dashboard')
    try:
        approved_user_profile.save()
        Admission_Query.objects.get(pk=pk).delete()
        messages.success(request, 'Student approved and registered successfully !')
        return redirect('admission_requests')
    except:
        messages.error(request, "Failed to register !")
        return redirect('admission_requests')







    
