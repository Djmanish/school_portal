from django.shortcuts import render, HttpResponse, redirect
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



# Create your views here.

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

    


@login_required
def edit_profile(request, pk):
    user_info = UserProfile.objects.get(pk=pk)
    all_institutes = Institute.objects.all()
    all_states = State.objects.all()
    

    if request.method == "POST":
        new_admin = 'admin_check'  in request.POST
        if new_admin: #if admin checkbox is checked
            new_create_institute = Institute.objects.create(name=request.POST['new_institute_name'],
            Contact_number= request.POST['new_institute_phone'],
            address = request.POST['new_institute_address'])
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
        # creating row in role_description table
        new_level = Role_Description.objects.create(user=request.user, institute= updated_institute, level= up_level  )
        return redirect('user_profile')
        
    return render(request, 'main_app/edit_profile.html', {'user_info':user_info, 'all_institutes':all_institutes, 'all_states':all_states,})

