from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from main_app.models import*
from .models import *
from django.contrib import messages
from django.utils import timezone
from notices.models import *
from datetime import datetime, timedelta



# Create your views here.
def library(request):
    institute_data=Institute.objects.get(pk = request.user.profile.institute.id)
    categories= BookCategory.objects.filter(institute_category=request.user.profile.institute)
    sub_categories= BookSubCategory.objects.filter(institute_subcategory=request.user.profile.institute)
    #?
    total_books = Book.objects.filter(book_institute=request.user.profile.institute).count()
    total_issue = IssueBook.objects.filter(issue_book_institute=request.user.profile.institute,return_date__isnull=True)
    total_issue_books = total_issue.count()
    left = total_books - total_issue_books
    books= BookCode.objects.filter(book_institute=request.user.profile.institute)
    lib_set= LibrarySettings.objects.get(institute=request.user.profile.institute)
    
     # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
    context_data = {
      'institute_data':institute_data,
      'categories':categories, 
      'books':books,   
      'sub_categories':sub_categories,
      'total_books':total_books,
      'total_issue_books':total_issue_books,
      'left':left,
      'total_issue':total_issue,
      'lib_set':lib_set,
    }
    return render(request, 'library/library.html',context_data)

def book(request):
    institute_data=Institute.objects.get(pk=request.user.profile.institute.id)
    categories= BookCategory.objects.filter(institute_category=request.user.profile.institute)
    sub_categories= BookSubCategory.objects.filter(institute_subcategory=request.user.profile.institute)
    books= BookCode.objects.filter(book_institute=request.user.profile.institute)
    len_books=len(books)
     # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
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
                  messages.success(request, 'Book group added successfully !')
                  messages.info(request, "Please enter book ids !")
                  return HttpResponseRedirect(f'/library/add_book/?book_group={new_book.id}')
            else:                  
                  messages.error(request, 'Book code already added !')
                  messages.info(request, "Please try another book code !")
                  return HttpResponseRedirect(f'/library/book/')
            
              
            
      

def add_book(request):  
      institute_data=Institute.objects.get(pk=request.user.profile.institute.id)
      book_code= BookCode.objects.get(pk=request.GET.get('book_group'))  
      book_count = int(book_code.book_count)
       # starting user notice
      if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
      # ending user notice
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
                        i = i.strip()
                        search_book= Book.objects.get(book_id=i)
                        
                  messages.error(request, "Book ids must be unique !")                        
                  return HttpResponseRedirect(f'/library/')
                        
                except:


                  for id in book_ids:   
                        id = id.strip()                     
                        Book.objects.create(book_id=id, book_code=book_code.code, book_institute=book_code.book_institute, book_name=book_code.book_name, book_category=book_code.book_category, book_sub_category=book_code.book_sub_category, author=book_code.author, publications=book_code.publications, edition=book_code.edition, book_count=book_count_len )
                  messages.success(request, 'Books added successfully !')
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
    messages.success(request, 'Sub category created successfully !')
    return HttpResponseRedirect(f'/library/')

def issuebook(request):
      designation=Institute_levels.objects.filter(institute=request.user.profile.institute)
      if request.method == 'POST':
            role= request.POST['selected_role']
            name= request.POST['full_name']
            print(role)
      # starting user notice
      if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
      # ending user notice
      context_data = {
        'designation':designation,      
      }
      return render(request, 'library/issue.html',context_data)

def fetch_user_data(request):
      if request.method == 'POST':
            role= request.POST['selected_designation']
            name= request.POST['selected_name']
            if role == "100":
                  q1= UserProfile.objects.filter(institute=request.user.profile.institute,first_name__icontains=name)
                  q2= q1.exclude(designation__level_name="student")
                  user_data = q2.exclude(designation__level_name="parent")
                  des=1
                  
            else:                  
                designation=Institute_levels.objects.get(pk=role, institute=request.user.profile.institute)
                user_data= UserProfile.objects.filter(designation=designation, institute=request.user.profile.institute ,  first_name__icontains=name)
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
          sh_for_days = LibrarySettings.objects.get(institute__id=request.user.profile.institute.id)
          today= timezone.now()
          expirydate= today+timedelta(days= sh_for_days.day_Span)
          ex_d =expirydate.date()
          # expirydate= request.POST['return_date']
          borrower= UserProfile.objects.get(pk=userid)
          try:
            borrower_book= Book.objects.get(book_id=bookid)
          except Book.DoesNotExist:
            messages.error(request, 'Incorrect book id')
            return HttpResponseRedirect(f'/library/issuebook/')
          try:
            chk= IssueBook.objects.get(book_name__book_id=bookid, return_date__isnull=True)
            messages.error(request, 'Book is already issued')
            return HttpResponseRedirect(f'/library/issuebook/')
          except:
            
            # today_time= datetime.datetime.now().strftime('%H:%M:%S')
            new_issue_book=IssueBook.objects.create(user_name=borrower, book_name=borrower_book, issue_book_institute=borrower.institute, issued_by=request.user.profile, issued_date=today, expiry_date=expirydate)
            messages.success(request, 'Book issued successfully !')
            messages.info(request,f' Return date is {ex_d} !')
            return HttpResponseRedirect(f'/library/issuebook/')
          
      # return HttpResponse('Hello World Issue Book')      


def book_return(request):
      if request.method == 'POST':
            print("Book Return method")
            book_i= request.POST.get('borrow_id') 
            cat= request.POST.get('book_category')  
            if cat == "0":  
              messages.error(request, 'Book Not Returned, Please Try Again !')
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
              messages.success(request, 'Book returned successfully !')
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

def fetch_sub_category(request):
    selected_category  = BookCategory.objects.get(pk=request.POST.get('category'))
    
    category_search = BookSubCategory.objects.filter(parent_category__pk=selected_category.id)
    subs = ""
    for sub in category_search:
        subs= subs+ f"<option value='{sub.id}' >"+str(sub)+"</option>"
    return HttpResponse(subs)
      
def lib_settings(request):
      if request.method == 'POST':
            max_b= request.POST['max_books']
            days_b= request.POST['days_books']
            reminder_d= request.POST['reminder_days']            
            t= LibrarySettings.objects.get(institute__id=request.user.profile.institute.id)
            t.max_Book_Allows= max_b
            t.day_Span= days_b
            t.send_Reminder_Before= reminder_d
            t.save()              
            return HttpResponseRedirect(f'/library/')        

