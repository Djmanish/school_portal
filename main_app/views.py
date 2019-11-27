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
    




@login_required
def edit_profile(request, pk):
    user_info = UserProfile.objects.get(pk=pk)
    all_institutes = Institute.objects.all()

    if request.method == "POST":
        print('post method')
    return render(request, 'main_app/edit_profile.html', {'user_info':user_info, 'all_institutes':all_institutes})