from django.shortcuts import render
from main_app import views
from main_app import templates

# Create your views here.
def attendance(request):    
    return render(request, 'main_app/Attendence.html')