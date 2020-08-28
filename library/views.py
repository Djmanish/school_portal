from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from main_app.models import*
from .models import *
from django.contrib import messages
from django.utils import timezone
from notices.models import *
from datetime import datetime, timedelta
from library.utils import render_to_pdf
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from library.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token




# Create your views here.
def library(request):
    institute_data=Institute.objects.get(pk = request.user.profile.institute.id)
    categories= BookCategory.objects.filter(institute_category=request.user.profile.institute)
    sub_categories= BookSubCategory.objects.filter(institute_subcategory=request.user.profile.institute)
    #?
    total_books = Book.objects.filter(book_institute=request.user.profile.institute, status="active").count()
    total_issue = IssueBook.objects.filter(issue_book_institute=request.user.profile.institute,return_date__isnull=True)
    total_issue_books = total_issue.count()
    left = total_books - total_issue_books
    books= BookCode.objects.filter(book_institute=request.user.profile.institute, status = "active")
    for b in books:
          sh_books= Book.objects.filter(book_code=b.code, book_institute=b.book_institute,status="active").count()
          b.count=sh_books
    try:
          lib_set= LibrarySettings.objects.get(institute=request.user.profile.institute)
    except LibrarySettings.DoesNotExist:
          lib_set = LibrarySettings.objects.create(institute=request.user.profile.institute, max_Book_Allows=3, day_Span=5, send_Reminder_Before=2, late_fine_per_day=5)
    cat = BookCategory.objects.filter(institute_category=request.user.profile.institute)
    for i in cat:
          i.name= i
          i.sub = BookSubCategory.objects.filter(parent_category=i.name, institute_subcategory=request.user.profile.institute)
    
     # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
    context_data = {
      'cat':cat,
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

def checkIfDuplicates_1(listOfElems):
    # ''' Check if given list contains any duplicates '''
    if len(listOfElems) == len(set(listOfElems)):
      return False
    else:
      return True

      
def add_new_book(request):
      if request.method == 'POST':
                book_ids= request.POST.getlist('fullname')
                book_count_len=len(book_ids)
                book_code= BookCode.objects.get(pk=request.POST.get('hide'))
                result= checkIfDuplicates_1(book_ids)
                if result:
                      messages.error(request, "You are entering same book id's !")  
                      instance = BookCode.objects.get(id=book_code.id, book_institute=request.user.profile.institute)
                      instance.delete()
                      return HttpResponseRedirect(f'/library/') 
                else:
                      print ("non Duplicates")
                for book in book_ids:
                      try:
                        search_books= Book.objects.get(book_id=book, book_institute=request.user.profile.institute)
                        messages.error(request, "Books id's must be unique !") 
                        return HttpResponseRedirect(f'/library/') 
                      except:
                        pass
                
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
              messages.success(request, 'Category created successfully !')
            except:
              messages.error(request, 'Category already exists !')
              
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
            borrower_book= Book.objects.get(book_id=bookid, book_institute=request.user.profile.institute)
          except Book.DoesNotExist:
            messages.error(request, 'Incorrect book id !')
            return HttpResponseRedirect(f'/library/issuebook/')
          try:
            chk= IssueBook.objects.get(book_name__book_id=bookid, return_date__isnull=True)
            messages.error(request, 'Book is already issued !')
            return HttpResponseRedirect(f'/library/issuebook/')
          except:
            chk_active_issue= sh_for_days.max_Book_Allows
            sch_user= IssueBook.objects.filter(user_name=borrower,issue_book_institute=borrower.institute,return_date__isnull=True).count()
            print(sch_user)
            print(chk_active_issue)
            # today_time= datetime.datetime.now().strftime('%H:%M:%S')
            if sch_user < chk_active_issue:
              new_issue_book=IssueBook.objects.create(user_name=borrower, book_name=borrower_book, issue_book_institute=borrower.institute, issued_by=request.user.profile, issued_date=today, expiry_date=expirydate)
              messages.success(request, 'Book issued successfully !')
              messages.info(request,f' Return date is {ex_d} !')
              return HttpResponseRedirect(f'/library/issuebook/')
            else:                  
                  messages.error(request, 'Requested user active issued book limit is exceeded !')  
                  return HttpResponseRedirect(f'/library/issuebook/')
          
      # return HttpResponse('Hello World Issue Book')      


def book_return(request):
      if request.method == 'POST':
            lib = LibrarySettings.objects.get(institute__id=request.user.profile.institute.id)
            book_i= request.POST.get('borrow_id') 
            cat= request.POST.get('book_category') 
            fine= request.POST.get('book_fine') 
            desc= request.POST.get('book_desc')
            if fine:
                  pass
            else:
                  fine = 0
            print(fine)
            if cat == "0":  
              messages.error(request, 'Book not returned, please try again !')
            else:      
              t = IssueBook.objects.get(id=book_i)
              cd = t.expiry_date           
              td = timezone.now()

              if td > cd :
                    cc= (td - cd).days
                    lt_fine = int(cc*lib.late_fine_per_day)
              else:
                    cc = 0
                    lt_fine = 0
              
              t.return_date = timezone.now()            
              t.delay_counter=cc
              t.late_fine = lt_fine
              t.damage_fine = int(fine)
              t.description= desc
              t.updated_by= request.user.profile
              t.date= td
              t.save()
              messages.success(request, 'Book returned successfully !')
            return HttpResponseRedirect(f'/library/')
            

      
      
def return_book(request):
      if request.method == 'POST':
            bookid= request.POST.get('issue_dt')
            # search_book_rt= Book.objects.get(book_id=bookid)
            issue_book_search= IssueBook.objects.get(book_name__book_id=bookid,issue_book_institute=request.user.profile.institute,  return_date__isnull=True)
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
            messages.success(request, 'Library settings updated successfully !')    
            return HttpResponseRedirect(f'/library/')        

def edit_book(request):
      if request.method == "POST": 
            book_cid = request.POST['book_id']
            search_edit_book= BookCode.objects.get(pk=book_cid)
            search_books= Book.objects.filter(book_code=search_edit_book.code)
            name = request.POST['book_name']
            category = request.POST['book_category']
            sch_cat = BookCategory.objects.get(pk=category)
            edit_sub_category = request.POST['book_sub_category']
            sch_sub_cat = BookSubCategory.objects.get(pk=edit_sub_category)
            author = request.POST['author_name']
            pub = request.POST['publications']
            edition = request.POST['editions']
            # BookCode Group Section
            search_edit_book.book_name = name
            search_edit_book.book_category = sch_cat
            search_edit_book.book_sub_category = sch_sub_cat
            search_edit_book.author = author
            search_edit_book.publications = pub
            search_edit_book.edition = edition
            search_edit_book.save()
            for i in search_books:
              i.book_name = name
              i.book_category = sch_cat
              i.book_sub_category = sch_sub_cat
              i.author = author
              i.publications = pub
              i.edition = edition
              i.save()        
            messages.success(request, 'Books info updated successfully !')    
      return HttpResponseRedirect(f'/library/')

def delete_book(request,pk):
      search_edit_book= BookCode.objects.get(pk=pk)
      
      search_books= Book.objects.filter(book_code=search_edit_book.code)
      for i in search_books:
            try:
                  ser_bk = IssueBook.objects.get(book_name__id= i.id, return_date__isnull=True)
                  messages.error(request,f'Unable to delete, Book ID: {i.book_id} is issued !')
                  return HttpResponseRedirect(f'/library/')
            except IssueBook.DoesNotExist:
                  pass
      for i in search_books:
            i.status = "inactive"
            i.save()
      search_edit_book.status = "inactive"
      search_edit_book.save()
      messages.error(request,f'Book code:- {search_edit_book}, deleted successfully !')
      return HttpResponseRedirect(f'/library/')

def add_more_books(request):
      if request.method == 'POST':
        institute_data=Institute.objects.get(pk=request.user.profile.institute.id)
        book_code= BookCode.objects.get(pk=request.POST.get('book_code_hidden')) 
        copies_books = Book.objects.filter(book_code=book_code.code, book_institute= request.user.profile.institute)
        copies= copies_books.count()
        new_copies = int(request.POST.get('add_more_books'))
        context_data = {
        'institute_data':institute_data,  
        'book_code':book_code,
        'copies':copies,
        'copies_books':copies_books,
        'range':range(new_copies),
        }
      return render(request, 'library/add_more_copies.html', context_data)

def add_new_books(request):
      if request.method == 'POST':            
            book_ids= request.POST.getlist('fullname')
            book_count_len=len(book_ids)
            book_code= BookCode.objects.get(pk=request.POST.get('hide'))
            res= checkIfDuplicates_1(book_ids)
            
            if res:
                  messages.error(request, "You are entering same book id's !")  
                  return HttpResponseRedirect(f'/library/') 
            else:
                  print ("non Duplicates")
            for book in book_ids:
                      try:
                        search_books= Book.objects.get(book_id=book, book_institute=request.user.profile.institute)
                        messages.error(request, "Books id's must be unique !") 
                        return HttpResponseRedirect(f'/library/') 
                      except:
                        pass
            for id in book_ids:
                      id = id.strip()                        
                      Book.objects.create(book_id=id, book_code=book_code.code, book_institute=book_code.book_institute, book_name=book_code.book_name, book_category=book_code.book_category, book_sub_category=book_code.book_sub_category, author=book_code.author, publications=book_code.publications, edition=book_code.edition, book_count=book_count_len )
            messages.success(request, 'Books added successfully !')
            return HttpResponseRedirect(f'/library/')

def see_all(request):
      return HttpResponse('See all Book')
            

def show_qr(request):
      if 'selected_individual' in request.POST:
            print("Hello World")
            institute_data = request.user.profile.institute
            selected_books = request.POST.getlist('selected_individual')
                       
            selected_individuals_list = []
            for i in selected_books: #test this
                  selected_individuals_list.append(Book.objects.get(pk=i,status="active", book_institute=request.user.profile.institute))
            length = len(selected_individuals_list)
            if length  == 5:
                  rows = 1
            else:
                  if length%5 == 0:
                        rows = int((length/5))
                  else:
                        rows = int((length/5)+1)
            q = []
            col = 5
            intial = 0
            for i in range(rows):
                  q.append((selected_individuals_list)[intial:col])
                  intial = col
                  col = col+5
            for i in q:
                  print(i)                  
            return render_to_pdf(
                  'library/all_book_pdf.html',
                  {
                        'pagesize':'A4',
                        'wishlist': q,
                        'institute_data':institute_data,
                    }
                  )

      if 'all_classes_check' in request.POST:
            print("Nothng")
            institute_data = request.user.profile.institute
            results= Book.objects.filter(status="active", book_institute=request.user.profile.institute)
            if results.count() <= 5:
                  r = 1
            else:
                  if results.count()%5 == 0:
                        r = int((results.count()/5)) 
                  else:
                        r = int((results.count()/5)+1) 
            
            q = []
            col = 5
            initial = 0
            for i in range(r):
                  print("Hello world")
                  q.append((results)[initial:col])  
                  initial = col
                  col = col+5  
            for i in q:
                  print(i)       
            return render_to_pdf(
                  'library/all_book_pdf.html',
                  {
                        'pagesize':'A4',
                        'mylist': q,
                        'institute_data':institute_data,
                        
                    }
                  )
      
def view_book(request, pk):
      institute_data=Institute.objects.get(pk = request.user.profile.institute.id)
      total_books = Book.objects.filter(book_institute=request.user.profile.institute, status="active").count()
      total_issue = IssueBook.objects.filter(issue_book_institute=request.user.profile.institute,return_date__isnull=True)
      total_issue_books = total_issue.count()
      left = total_books - total_issue_books
      try:
            book_grp= BookCode.objects.get(pk=pk, book_institute=request.user.profile.institute)
      except BookCode.DoesNotExist:
            messages.error(request,f'Requested book not found !')
            return HttpResponseRedirect(f'/library/')
      
      grp_books= Book.objects.filter(book_code=book_grp.code, book_institute=request.user.profile.institute, status="active")
      
      context_data = {
      'institute_data':institute_data,
      'total_books':total_books,
      'total_issue_books':total_issue_books,
      'left':left,
      'book_grp':book_grp,
      'grp_books':grp_books,   
    }
      return render(request, 'library/view_book.html',context_data)

def delete_view_book(request, pk):
      delete_bk= Book.objects.get(pk=pk)
      book_cd = BookCode.objects.get(code=delete_bk.book_code, book_institute=request.user.profile.institute)
      idd = book_cd.pk
      try:
            search_book = IssueBook.objects.get(book_name__id=delete_bk.id, return_date__isnull=True)
            messages.error(request,f'Unable to delete, book id: {delete_bk.book_id} is issued !')
            return HttpResponseRedirect(f'/library/view_book/{idd}')
      except IssueBook.DoesNotExist:
            print("hello")
            delete_bk.status="inactive"
            delete_bk.save()      
            messages.error(request,f'Book deleted successfully !')
            return HttpResponseRedirect(f'/library/view_book/{idd}')

def fetch_book_ids(request):
      selected_book_code = BookCode.objects.get(pk=request.POST.get('class_id') )
      search_books = Book.objects.filter(book_code=selected_book_code.code, status="active",book_institute=request.user.profile.institute)
      individual_options = ''
      for individual in search_books:
            individual_options = individual_options+f"<option value='{individual.id}'>{individual.book_id} - {individual.book_name}</option>"
     
      return HttpResponse(individual_options)

class UserCreate(APIView):
    """ 
    Creates the user. 
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

