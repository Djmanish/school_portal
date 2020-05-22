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
    books= Book.objects.filter(book_institute=request.user.profile.institute)
    len_books=len(books)
    context_data = {
      'institute_data':institute_data,  
      'categories':categories,
      'sub_categories':sub_categories,
      'books':books,
      'len_books':len_books,
      }
    return render(request, 'library/add_book.html',context_data)

def add_book_group(request):
      if request.method == 'POST':
            new_book_code= request.POST['book_code'].strip()
            new_book_count= request.POST['book_count'].strip()
            new_book_name= request.POST['book_name']
            new_book_category= request.POST['book_category']
            new_book_subcategory= request.POST['book_sub_category']
            new_book_author= request.POST['author_name']
            new_book_publication= request.POST['publications']
            new_book_edition= request.POST['editions']
            get_category= BookCategory.objects.get(id=new_book_category)
            get_subcategory= BookSubCategory.objects.get(id=new_book_subcategory)
            ins=request.user.profile.institute
            try:
              search_code= BookCode.objects.get(book_institute=ins, code= new_book_code)
            except BookCode.DoesNotExist:
              search_code=0
            if search_code == 0:
                  new_book= BookCode.objects.create(code=new_book_code, book_count=new_book_count, book_institute=ins, book_name=new_book_name, book_category=get_category, book_sub_category=get_subcategory, author=new_book_author, publications=new_book_publication, edition=new_book_edition)
                  messages.success(request, 'Book Group Added successfully !')
                  messages.info(request, "Please Enter Book ID's !")
                  return HttpResponseRedirect(f'/library/add_book/?book_group={new_book.id}')
            else:                  
                  messages.error(request, 'Book Code Already Added !')
                  messages.info(request, "Please Try Another Book Code !")
                  return HttpResponseRedirect(f'/library/book/')
            
              
            
      

def add_book(request):  
      institute_data=Institute.objects.get(pk=request.user.profile.institute.id)
      book_code= BookCode.objects.get(pk=request.GET.get('book_group'))  
      book_count = int(book_code.book_count)
      context_data = {
      'institute_data':institute_data,  
      'book_code':book_code,
      'range':range(book_count),
      }


      return render(request, 'library/add_book_copies.html', context_data)
      
def add_new_book(request):
      if request.method == 'POST':
                book_ids= request.POST.getlist('fullname')
                book_count_len=len(book_ids)
                book_code= BookCode.objects.get(pk=request.POST.get('hide'))
                try:
                  for i in book_ids:
                        search_book= Book.objects.get(book_id=i)
                        print(search_book)
                  messages.error(request, "Books Id's Must Be Unique !")                        
                  return HttpResponseRedirect(f'/library/book/')
                        
                except:


                  for id in book_ids:                        
                        Book.objects.create(book_id=id, book_code=book_code.code, book_institute=book_code.book_institute, book_name=book_code.book_name, book_category=book_code.book_category, book_sub_category=book_code.book_sub_category, author=book_code.author, publications=book_code.publications, edition=book_code.edition, book_count=book_count_len )
                  messages.success(request, 'Books Added successfully !')
                  return HttpResponseRedirect(f'/library/book/')

            

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

def issuebook(request):
      designation=Institute_levels.objects.filter(institute=request.user.profile.institute)
      if request.method == 'POST':
            role= request.POST['selected_role']
            name= request.POST['full_name']
            print(role)
     
      context_data = {
        'designation':designation,      
      }
      return render(request, 'library/issue.html',context_data)

def fetch_user_data(request):
      if request.method == 'POST':
            role= request.POST['selected_designation']
            name= request.POST['selected_name']
            designation=Institute_levels.objects.get(pk=role, institute=request.user.profile.institute)

            user_data= UserProfile.objects.filter(designation=designation, first_name__icontains=name)
            context_data = {
              'user_data':user_data
            }
            return render(request, 'library/user_search.html', context_data)

def issue_book(request):
      if request.method == 'POST':
          userid= request.POST['user_id']
          bookid= request.POST['book_id']
          expirydate= request.POST['return_date']
          borrower= UserProfile.objects.get(pk=userid)
          borrower_book= Book.objects.get(book_id=bookid)
          today= datetime.datetime.today()
          today_time= datetime.datetime.now().strftime('%H:%M:%S')
          new_issue_book=IssueBook.objects.create(user_name=borrower, book_name=borrower_book, issue_book_institute=borrower.institute, issued_by=request.user.profile, issued_date=today, expiry_date=expirydate)
          messages.success(request, 'Book Issued Successfully !')
          return HttpResponseRedirect(f'/library/')
          
      # return HttpResponse('Hello World Issue Book')      


def user_id_data(request):
      print("Hello World")
      if request.method == 'POST':
            user_d= request.POST['user_id'] 
            user_pro= UserProfile.objects.get(pk=user_d)
            print(user_pro)
            context_data = {
              'user_pro':user_pro,
            }
            return render(request, 'library/user_id_data.html', context_data)
      
      

