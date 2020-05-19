from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from main_app.models import*
from .models import *
from django.contrib import messages

# Create your views here.
def library(request):
    institute_data=Institute.objects.get(name=request.user.profile.institute)
    inst=request.user.profile.institute
    categories= BookCategory.objects.filter(institute_category=inst)
    context_data = {'institute_data':institute_data, 
    
      }
    return render(request, 'library/library.html',context_data)

def book(request):
    return render(request, 'library/add_book.html')

def add_category(request):
      if request.method == 'POST':
            category= request.POST['book_category_name']
            try:
              new_category= BookCategory.objects.create(book_category_name=category, institute_category=request.user.profile.institute)
              messages.success(request, 'Category Created successfully !!!')
            except:
              messages.error(request, 'Category Already Exists !!!')
              
            return HttpResponseRedirect(f'/library/')           
      
      

