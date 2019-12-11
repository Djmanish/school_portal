from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db.models import Q





# Create your views here.


def approvals(request):
    pending_users= UserProfile.objects.filter(status='pending')
    active_users= UserProfile.objects.filter(status='approve')
    inactive_users= UserProfile.objects.filter(status='dissapprove')
    return render(request, 'main_app/Approvals.html', {'Pending_user':pending_users,'Active_user':active_users,'Inactive_user':inactive_users})

def index(request):
    return render(request, 'main_app/index.html')

@login_required
def dashboard(request):
    return render(request, 'main_app/dashboard.html')


class RegistrationViewUniqueEmail(RegistrationView):
    form_class = RegistrationFormUniqueEmail

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            g_user = User.objects.get(email= username) # checkng whether user registered or not ?
            try:
                if g_user.is_active == False: # checking if user activated his account or not
                    error = 'User already registered, check your mail and follow the link to activate your account.'
                    return render(request, 'registration/login.html', {'error':error})
                else:
                    username = g_user.username
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('user_dashboard')
                else:
                    error = 'Email or password incorrect'
                    return render(request, 'registration/login.html', {'error':error})
            except:
                error = 'Email or password incorrect'
                return render(request, 'registration/login.html', {'error':error})               
        except:
            error = 'No user registered with this email !'
            return render(request, 'registration/login.html', {'error':error})
    else:
        return render(request, 'registration/login.html')

@login_required
def user_profile(request):
    return render(request, 'main_app/admin_user_profile.html')
    
  
    
    
def fetch_levels(request):
    id = request.POST['school_id']
    levels = Institute_levels.objects.filter( institute = id)
    nlevels=""
    for t in levels:
        nlevels= nlevels+ f"<option value='{t.id}' >"+str(t)+"</option>"
    return HttpResponse(nlevels)

    
def edit_institute(request, pk):
    institute_info =Institute.objects.get(pk=pk)




    

@login_required
def edit_profile(request, pk):
    user_info = UserProfile.objects.get(pk=pk)
    all_institutes = Institute.objects.all()
    all_states = State.objects.all()
    
    if request.method == "POST":
        new_admin = 'admin_check'  in request.POST
        if new_admin: #if admin checkbox is checked
            try:
                new_create_institute = Institute.objects.create(name=request.POST['new_institute_name'],
            contact_number1= request.POST['new_institute_phone'],
            address1 = request.POST['new_institute_address'],
            created_by = request.user) # creating new institute
            except:
                messages.info(request, 'Institute already exists !!!')
                return render(request, 'main_app/edit_profile.html', {'user_info':user_info, 'all_institutes':all_institutes, 'all_states':all_states,})
            
            new_level = Institute_levels.objects.create(institute=new_create_institute, level_id=1, level_name='admin')
            new_level = Institute_levels.objects.create(institute=new_create_institute, level_id=2, level_name='parent') 
            new_level = Institute_levels.objects.create(institute=new_create_institute, level_id=3, level_name='student')# creating default level for admin
            role = Role_Description.objects.create(user=request.user, institute=new_create_institute, level= new_level) # creating default role for admin
            user_info.designation = new_level
            user_info.institute= new_create_institute
            user_info.save()
        else:
            pass
        
        user_info.first_name= request.POST['first_name']
        user_info.middle_name= request.POST['middle_name']
        user_info.last_name= request.POST['last_name']
        user_info.date_of_birth= request.POST['dob']
        if 'select_school' in request.POST: # checking if new admin select box is checked and selected institute
            selected_institute_pk = request.POST['select_school']
            updated_institute = Institute.objects.get(pk=selected_institute_pk) #fetching the selected institutes list
            user_info.institute= updated_institute
        if 'user_designation' in request.POST: 
            level_id = request.POST['user_designation']
            up_level= Institute_levels.objects.get(pk=level_id) # fetching the selected level the levels list
            user_info.designation = up_level
            new_level = Role_Description.objects.create(user=request.user, institute= updated_institute, level= up_level  )

        user_info.about= request.POST['about']
        if 'profile_pic' in request.FILES:
            user_info.profile_pic= request.FILES['profile_pic']
        
        user_info.mobile_number= request.POST['mobile_number']
        user_info.address_line_1= request.POST['address_line_1']
        user_info.address_line_2= request.POST['address_line_2']
        user_info.city= request.POST['city']
        if 'state' in request.POST:
            updated_state= State.objects.get(pk=request.POST['state'])
            user_info.state= updated_state 
        
        user_info.facebook_link= request.POST['facebook_link']
        user_info.save()
        
        messages.success(request, 'Profile details updated.')
        return redirect('user_profile')
        
    return render(request, 'main_app/edit_profile.html', {'user_info':user_info, 'all_institutes':all_institutes, 'all_states':all_states,})


  

@login_required
def institute_profile(request, pk):
    institute_data= Institute.objects.get(pk=pk)
    institute_roles = Institute_levels.objects.filter(institute=institute_data).reverse()
    
    
    return render(request, 'main_app/institute_profile.html', {'institute_data':institute_data, 'institute_roles':institute_roles})
   
@login_required
def edit_institute(request, pk):
    edit_institute= Institute.objects.get(pk=pk)
    return render(request, 'main_app/edit_institute.html', {'edit_institute':edit_institute})
   

class InstituteUpdateview(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Institute
    
    fields = ['code','name','establish_date', 'profile_pic','principal','about','contact_number1','contact_number2','contact_number3','address1','address2','district','state','country','pin_code','email','facebook_link','website_link']

    template_name="main_app/edit_institute.html"
    success_message = "Details were updated successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    def get_success_url(self, **kwargs):         
        return reverse_lazy("institute_detail", kwargs={'pk':self.request.user.profile.institute.id})



def approve_request(request, pk):
    user = UserProfile.objects.get(pk=pk)
    user.approve()
    return redirect('approvals')

def disapprove_request(request, pk):
    user = UserProfile.objects.get(pk=pk)
    user.disapprove()
    return redirect('approvals')

def add_new_role(request, pk):
    if request.method== "POST":
        institute = Institute.objects.get(pk=pk)
    
        new_role = Institute_levels()
        new_role.institute= institute
        new_role.level_id = request.POST['level_id']
        new_role.level_name = request.POST['level_name']
        rr= institute.id
        try:
            roles_level_toi = Institute_levels.objects.filter(Q(institute = institute) & Q(level_id__gte =  request.POST['level_id'] )  )
            for role in roles_level_toi: 
                role.level_id += 1
                role.save()
            new_role.save()
            messages.success(request, "New Role Added Successfully !")
            return HttpResponseRedirect(f'/institute/profile/{rr}/')  
        except:
            messages.info(request, "Failed to Add, check you fields!")
            return HttpResponseRedirect(f'/institute/profile/{rr}/')
  
    else:
         return HttpResponseRedirect(f'/institute/profile/{rr}/')

def delete_user_role(request, pk):
    
    user_role =  Institute_levels.objects.get(pk=pk, institute= request.user.profile.institute)
    role_id= user_role.level_id
    if user_role.level_name == 'admin'  or user_role.level_name == 'parent' or user_role.level_name == 'student' :
        messages.warning(request, 'Admin, Parent or student roles can not be deleted !!!')
        rr= request.user.profile.institute.id
        return HttpResponseRedirect(f'/institute/profile/{rr}/')
    else:
        roles_level_tod = Institute_levels.objects.filter(Q(institute = user_role.institute) & Q(level_id__gte =  user_role.level_id )  )
        for roles in roles_level_tod:
            roles.level_id -= 1
            roles.save()
        user_role.delete()
        messages.success(request, 'User role deleted successfully !')
        rr= request.user.profile.institute.id
        return HttpResponseRedirect(f'/institute/profile/{rr}/')


    

    



    

