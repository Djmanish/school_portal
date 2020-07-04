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
        Student_Photo= request.FILES.get('student_pic')
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
        new_request.date_of_birth = request.POST.get('dob')
        new_request.student_blood_group = request.POST.get('student_blood_group')
        new_request.gender = request.POST.get('gender')
        new_request.school_name = Institute.objects.get(pk= request.POST.get('school'))
        new_request.class_name = Classes.objects.get(pk=request.POST.get('class'))
        new_request.mobile_Number = request.POST.get('mobile_number')
        new_request.Email_Id = request.POST.get('email')
        new_request.Nationality = request.POST.get('nationality')
        new_request.Address= request.POST.get('address').strip()
        new_request.District = request.POST.get('district').strip()
        new_request.state = State.objects.get(pk = request.POST.get('state'))
        new_request.country = request.POST.get('country').strip()
        new_request.Pin_Code = request.POST.get('pin_code')
        new_request.p_address= request.POST.get('p_address')
        new_request.p_district = request.POST.get('p_district')
        new_request.p_State = State.objects.get(pk=request.POST.get('p_state'))
        new_request.p_country = request.POST.get('p_country')
        new_request.p_pin_code = request.POST.get('p_pin_code')
        new_request.religion = request.POST.get('religion')
        new_request.category = request.POST.get('category')
        new_request.sub_cast = request.POST.get('sub_cast')
        new_request.student_aadhar_card = request.POST.get('student_aadhar_card')
        new_request.Student_Photo= request.FILES['student_pic']
        new_request.father_name = request.POST.get('father_name').strip()
        new_request.f_mobile_Number = request.POST.get('f_mobile_number')
        new_request.f_Email_Id = request.POST.get('f_Email_Id')
        new_request.f_aadhar_card = request.POST.get('f_aadhar_card')
        new_request.f_qualification = request.POST.get('f_qualification')
        new_request.f_occupation = request.POST.get('f_occupation')
        if 'f_photo' in request.FILES:
            new_request.f_photo= request.FILES['f_photo']
        if 'address_same' in request.POST:
            new_request.address_same= True
        if 'guardian_applicable' in request.POST:
            new_request.g_applicable= True

        new_request.mother_name = request.POST.get('mother_name').strip()
        new_request.m_mobile_Number = request.POST.get('m_mobile_number')
        new_request.m_Email_Id = request.POST.get('m_Email_Id')
        new_request.m_aadhar_card = request.POST.get('m_aadhar_card')
        new_request.m_qualification = request.POST.get('m_qualification')
        new_request.m_occupation = request.POST.get('m_occupation')
        if 'm_photo' in request.FILES:
            new_request.m_photo= request.FILES['m_photo']
        new_request.guardian_name = request.POST.get('guardian_name').strip()
        new_request.g_mobile_Number = request.POST.get('g_mobile_number')
        new_request.g_Email_Id = request.POST.get('g_Email_Id')
        new_request.g_aadhar_card = request.POST.get('g_aadhar_card')
        new_request.g_qualification = request.POST.get('g_qualification')
        new_request.g_occupation = request.POST.get('g_occupation')
        if 'g_photo' in request.FILES:
            new_request.g_photo= request.FILES['g_photo']
        if 'dob_certificate' in request.FILES:
            new_request.dob_certificate = request.FILES['dob_certificate']
        if 'id_proof_certificate' in request.FILES:
            new_request.id_proof_certificate = request.FILES['id_proof_certificate']
        if 'domicile_certificate' in request.FILES:
            new_request.domicile_certificate = request.FILES['domicile_certificate']
        if 'cast_certificate' in request.FILES:
            new_request.cast_certificate = request.FILES['cast_certificate']
        if 'character_certificate' in request.FILES:    
            new_request.character_certificate = request.FILES['character_certificate']
        if 'medical_certificate' in request.FILES:    
            new_request.medical_certificate = request.FILES['medical_certificate']
        if 'transfer_certificate' in request.FILES:    
            new_request.transfer_certificate = request.FILES['transfer_certificate']
        if 'last_year_certificate' in request.FILES:    
            new_request.last_year_certificate = request.FILES['last_year_certificate']
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
    classes = "<option selected disabled value="">-- Select class -- </option>"
    for Class in schools_all_classes:
        classes= classes+ f"<option value='{Class.id}' >"+str(Class)+"</option>"
    return HttpResponse(classes)
    

class Admission_Requests_View(LoginRequiredMixin, UserPassesTestMixin,  ListView ):
    model = Admission_Query
    template_name = "admissions/admission_requests.html"
    paginate_by = 25

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
        return Admission_Query.objects.filter(school_name= self.request.user.profile.institute).order_by('-id')

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
       
        #creating object of student info table for this student
        try:
            approved_user = Admission_Query.objects.filter(pk=pk).first()    
            Student_Info.objects.create(
                student = approved_user_profile,
                blood_group =  approved_user.student_blood_group,

                religion = approved_user.religion,
                sub_cast = approved_user.sub_cast,
                f_mobile_Number = approved_user.f_mobile_Number,
                f_Email_Id = approved_user.f_Email_Id,
                f_aadhar_card = approved_user.f_aadhar_card,
                f_qualification= approved_user.f_qualification,
                f_occupation = approved_user.f_occupation,
                f_photo= approved_user.f_photo,
                m_mobile_Number = approved_user.m_mobile_Number,
                m_Email_Id = approved_user.m_Email_Id,
                m_aadhar_card = approved_user.m_aadhar_card,
                m_qualification = approved_user.m_qualification,
                m_occupation = approved_user.m_occupation,
                m_photo = approved_user.m_photo,
                guardian_name = approved_user.guardian_name,
                guardian_mobile_Number = approved_user.g_mobile_Number,
                guardian_Email_Id = approved_user.g_Email_Id,
                guardian_aadhar_card = approved_user.g_aadhar_card,
                guardian_qualification = approved_user.g_qualification,
                guardian_occupation = approved_user.g_occupation,
                guardian_photo = approved_user.g_photo,
                guardian_applicable = approved_user.g_applicable,

                c_address = approved_user.Address,
                c_District = approved_user.District,
                c_state = approved_user.state,
                c_country = approved_user.country,
                c_Pin_Code = approved_user.Pin_Code,
                same_address =approved_user.address_same,
                p_address = approved_user.p_address,
                p_district =approved_user.p_district,
                p_State = approved_user.p_State,
                p_country = approved_user.p_country,
                p_pin_code = approved_user.p_pin_code,

                dob_certificate = approved_user.dob_certificate,
                id_proof_certificate = approved_user.id_proof_certificate,
                domicile_certificate = approved_user.domicile_certificate,
                cast_certificate = approved_user.cast_certificate,
                character_certificate = approved_user.character_certificate,
                medical_certificate = approved_user.medical_certificate,
                transfer_certificate = approved_user.transfer_certificate,
                last_year_certificate = approved_user.transfer_certificate,



            )
            
        except:
            print('failed')
        Admission_Query.objects.get(pk=pk).delete()
        messages.success(request, 'Student approved and registered successfully !')
        return redirect('admission_requests')
    except:
        messages.error(request, "Failed to register !")
        return redirect('admission_requests') 







    
