from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from main_app.models import*
from .models import *
from django.contrib import messages

# Create your views here.
def library(request):
    institute_data=Institute.objects.get(pk = request.user.profile.institute.id)
    categories= BookCategory.objects.filter(institute_category=request.user.profile.institute)#?
    context_data = {
      'institute_data':institute_data,
       'categories':categories,    
      }
    return render(request, 'library/library.html',context_data)

def book(request):
    institute_data=Institute.objects.get(pk=request.user.profile.institute.id)
    categories= BookCategory.objects.filter(institute_category=request.user.profile.institute)
    sub_categories= BookSubCategory.objects.filter(institute_subcategory=request.user.profile.institute)
    context_data = {
      'institute_data':institute_data,  
      'categories':categories,
      'sub_categories':sub_categories,
      }
    return render(request, 'library/add_book.html',context_data)

def add_book(request):
      if request.method == 'POST':
            new_book_code= request.POST['book_code'].strip()
            new_book_id= request.POST['book_id'].strip()
            new_book_name= request.POST['book_name']
            new_book_category= request.POST['book_category']
            new_book_subcategory= request.POST['book_sub_category']
            new_book_author= request.POST['author_name']
            new_book_publication= request.POST['publications']
            new_book_edition= request.POST['editions']
            get_category= BookCategory.objects.get(id=new_book_category)
            get_subcategory= BookSubCategory.objects.get(id=new_book_subcategory)
            ins=request.user.profile.institute
            new_book= Book.objects.create(book_code=new_book_code, book_id=new_book_id, book_institute=ins, book_name=new_book_name, book_category=get_category, book_sub_category=get_subcategory, author=new_book_author, publications=new_book_publication, edition=new_book_edition)
            messages.success(request, 'Book Added successfully !')
            return HttpResponseRedirect(f'/library/book')
            

def add_category(request):
      if request.method == 'POST':
            category= request.POST['book_category_name']
            try:
              new_category= BookCategory.objects.create(book_category_name=category, institute_category=request.user.profile.institute)
              messages.success(request, 'Category Created successfully !')
            except:
              messages.error(request, 'Category Already Exists !!!')
              
            return HttpResponseRedirect(f'/library/')    

def add_sub_category(request):    
  if request.method == 'POST':
    sub_category= request.POST['sub_category_name']  
    parent_categorys= request.POST['sub_category_parent']
    get_parent= BookCategory.objects.get(id=parent_categorys)
    print(get_parent)
    new_sub_category= BookSubCategory.objects.create(book_sub_category_name=sub_category, parent_category=get_parent, institute_subcategory=request.user.profile.institute)
    messages.success(request, 'Sub Category Created successfully !')
    return HttpResponseRedirect(f'/library/')
  
      
      

