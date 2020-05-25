from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from main_app.models import*
from .models import *
from django.contrib import messages
from django.utils import timezone


# Create your views here.
def library(request):
    institute_data=Institute.objects.get(pk = request.user.profile.institute.id)
    categories= BookCategory.objects.filter(institute_category=request.user.profile.institute)
    sub_categories= BookSubCategory.objects.filter(institute_subcategory=request.user.profile.institute)
    #?
    books= BookCode.objects.filter(book_institute=request.user.profile.institute)
    context_data = {
      'institute_data':institute_data,
      'categories':categories, 
      'books':books,   
      'sub_categories':sub_categories,
    }
    return render(request, 'library/library.html',context_data)

def book(request):
    institute_data=Institute.objects.get(pk=request.user.profile.institute.id)
    categories= BookCategory.objects.filter(institute_category=request.user.profile.institute)
    sub_categories= BookSubCategory.objects.filter(institute_subcategory=request.user.profile.institute)
    books= BookCode.objects.filter(book_institute=request.user.profile.institute)
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
                  messages.error(request, "Books Id's Must Be Uniqu !")                        
                  return HttpResponseRedirect(f'/library/')
                        
                except:


                  for id in book_ids:                        
                        Book.objects.create(book_id=id, book_code=book_code.code, book_institute=book_code.book_institute, book_name=book_code.book_name, book_category=book_code.book_category, book_sub_category=book_code.book_sub_category, author=book_code.author, publications=book_code.publications, edition=book_code.edition, book_count=book_count_len )
                  messages.success(request, 'Books Added successfully !')
                  return HttpResponseRedirect(f'/library/')

            

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
            if role == "100":
                  q1= UserProfile.objects.filter(first_name__icontains=name)
                  q2= q1.exclude(designation__level_name="student")
                  user_data= q2.exclude(designation__level_name="parent")
                  des=1
                  
            else:                  
                designation=Institute_levels.objects.get(pk=role, institute=request.user.profile.institute)
                user_data= UserProfile.objects.filter(designation=designation, first_name__icontains=name)
                des=0
            context_data = {
              'user_data':user_data,
              'des':des,
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
          return HttpResponseRedirect(f'/library/issuebook/')
          
      # return HttpResponse('Hello World Issue Book')      


def book_return(request):
      if request.method == 'POST':
            print("Book Return method")
            book_i= request.POST.get('borrow_id') 
            cat= request.POST.get('book_category')  
            if cat == "0":  
              messages.success(request, 'Book Not Returned, Please Try Again !')
            else:      
              t = IssueBook.objects.get(id=book_i)
              cd = t.expiry_date           
              td = timezone.now()
              if td > cd :
                    cc= (td - cd).days
              else:
                    cc = 0
              print(cc) 
              print(t)
              t.return_date = timezone.now()            
              t.delay_counter=cc
              t.save()
              messages.success(request, 'Book Returned Successfully !')
            return HttpResponseRedirect(f'/library/')
            

      
      
def return_book(request):
      if request.method == 'POST':
            bookid= request.POST.get('issue_dt')
            # search_book_rt= Book.objects.get(book_id=bookid)
            issue_book_search= IssueBook.objects.get(book_name__book_id=bookid,  return_date__isnull=True)
            # print(issue_book_search)
            context_data = {
              'issue_book_search':issue_book_search,
            }
            return render(request, 'library/book_return.html', context_data)
      
      

