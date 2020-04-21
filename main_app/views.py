from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, Http404, get_object_or_404
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
from class_schedule.models import *
from .forms import ClassUpdateForm, InstituteUpdateProfile
from django.core.mail import send_mail, send_mass_mail
from django.utils import timezone
from Attendance.models import *
from AddChild.models import *
from notices.models import *
from holidaylist.models import *
from django.contrib.sessions.models import Session
from examschedule.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main_app.serializers import UserProfileSerializer



class userList(APIView):

    def get(self, request):
        user1= UserProfile.objects.all()
        serializer = UserProfileSerializer(user1, many=True)
        return Response(serializer.data)
    
    def post(self):
        pass





# Create your views here.

def add_classes(request):
    user_permissions = request.user.user_institute_role.level.permissions.all()
    add_class_permission = App_functions.objects.get(function_name='Can Add Class')
    if add_class_permission in user_permissions:

       if request.method == "POST":
        class_name= request.POST['class_name']
        class_stage= request.POST.get('class_stage')
        
        new_class = Classes.objects.create(institute = request.user.profile.institute, name= class_name, class_stage= class_stage )
         #creating schedule for created class
        days=['Monday','Tuesday', 'Wednesday', 'Thursday','Friday','Saturday']
        for day in days:
            create_schedule = Schedule.objects.create(institute=request.user.profile.institute, Class= new_class, day= day )
        messages.success(request, 'Class Created successfully !!!')
        rr=request.user.profile.institute.id
        return HttpResponseRedirect(f'/institute/profile/{rr}/')
    else:
        messages.info(request, "you don't have permission to add class")
        return redirect('not_found')


class ClassUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Classes
    form_class = ClassUpdateForm
    template_name="main_app/edit_class.html"
    success_message = "Details were updated successfully !!!"
    

    def form_valid(self, form):
            form.instance.created_by = self.request.user
            return super().form_valid(form)
    def test_func(self):
        user_permissions = self.request.user.user_institute_role.level.permissions.all()
        can_edit_class_permission = App_functions.objects.get(function_name='Can Edit Class')
        if can_edit_class_permission in user_permissions:
            return True
        else:
            return False
    def get_success_url(self, **kwargs):         
            return reverse_lazy("institute_detail", kwargs={'pk':self.request.user.profile.institute.id})


# Add Subjects

def add_subjects(request):
    user_permissions = request.user.user_institute_role.level.permissions.all()
    add_subject_permission = App_functions.objects.get(function_name='Can Add Subject')
    if add_subject_permission in user_permissions:

        rr=request.user.profile.institute.id
        if request.method == "POST":
            subject_code= request.POST['subject_code']
            subject_name= request.POST['subject_name']
            new_class= request.POST['new_class']
            subject_teacher=request.POST['subject_teacher']
        
            # get data from Class Table
            subject_class=Classes.objects.get(id=new_class)
            # get data from User Table
            subject_teacher=User.objects.get(id=subject_teacher)

            subject_class = Subjects.objects.create(institute=request.user.profile.institute, subject_class=subject_class, subject_code= subject_code, subject_name= subject_name,subject_teacher=subject_teacher)

            messages.success(request, 'Subject Created successfully !!!')
            
        return HttpResponseRedirect(f'/institute/profile/{rr}/')


def edit_subject(request, pk):
    subject_to_edit = Subjects.objects.get(pk=pk)
    institute_classes = Classes.objects.filter(institute=request.user.profile.institute )
    designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='teacher')
    institute_teachers = UserProfile.objects.filter(institute= request.user.profile.institute, designation=designation_pk )

    user_permissions = request.user.user_institute_role.level.permissions.all()
    can_edit_subject_permission = App_functions.objects.get(function_name='Can Edit Subject')
 
    if can_edit_subject_permission in user_permissions:
        if request.method == 'POST':
            subject_class = Classes.objects.get(pk= request.POST.get('new_class'))
            new_subject_teacher = User.objects.get(pk= request.POST.get('subject_teacher'))

            new_subject_code =  request.POST.get('subject_code')
            new_subject_name = request.POST.get('subject_name')
        
            subject_to_edit.subject_class = subject_class
            subject_to_edit.subject_code = new_subject_code
            subject_to_edit.subject_name = new_subject_name
            subject_to_edit.subject_teacher=new_subject_teacher
            subject_to_edit.save()
            messages.success(request, 'Subject Updated Successfully !!!')
            institue_pk = request.user.profile.institute.pk
            return HttpResponseRedirect(f'/institute/profile/{institue_pk}')
    else:
        messages.info(request, "You Don't have permission to update subjects")
        return redirect('not_found')
    
    context = {
        'all_classes':institute_classes,
        'subject_info': subject_to_edit,
        'institute_teachers':institute_teachers
    }
    return render(request, 'main_app/edit_subject.html', context)

def delete_subject(request, pk):
        subject_to_delete = Subjects.objects.get(pk=pk)
        subject_to_delete.subject_code = "null"
        subject_to_delete.subject_name = "null"
        subject_to_delete.delete()
        messages.success(request, 'Subject Deleted Successfully !!!')
        institue_pk = request.user.profile.institute.pk
        return HttpResponseRedirect(f'/institute/profile/{institue_pk}')


def edit_class(request, pk):
    user_permissions = request.user.user_institute_role.level.permissions.all()
    can_edit_class_permission = App_functions.objects.get(function_name='Can Edit Class')
    if can_edit_class_permission in user_permissions:

        class_to_edit = Classes.objects.get(pk=pk)
        designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='teacher')
        institute_teachers = UserProfile.objects.filter(institute= request.user.profile.institute, designation=designation_pk )
        # institute_classes = Classes.objects.filter(institute=request.user.profile.institute)

        if request.method == 'POST':            
                new_class_teacher = User.objects.get(pk= request.POST.get('class_teacher'))
                class_to_edit.class_teacher = new_class_teacher
                new_edit_class =  request.POST.get('class_name')
                new_class_stage = request.POST.get('class_stage')
                class_to_edit.name = new_edit_class
                class_to_edit.class_stage = new_class_stage
                institue_pk = request.user.profile.institute.pk
                try:
                    class_to_edit.save()
                except:
                    messages.error(request, 'Teacher already assigned to a class !!!')
                    return HttpResponseRedirect(f'/institute/profile/{institue_pk}')
                messages.success(request, 'Class Updated Successfully !!!')
                
                return HttpResponseRedirect(f'/institute/profile/{institue_pk}')
    
        context = {
            'class_info': class_to_edit,
            'institute_teachers':institute_teachers
        }
        return render(request, 'main_app/edit_class.html', context)
    else:
        messages.info(request, 'May be you do not permission to edit classes')
        return redirect('not_found')

def delete_class(request, pk):
        class_to_delete = Classes.objects.get(pk=pk)
        class_to_delete.class_teacher = None
        class_to_delete.name = None
        class_to_delete.class_stage = None
        class_to_delete.delete()
        messages.success(request, 'Class Deleted Successfully !!!')
        institue_pk = request.user.profile.institute.pk
        return HttpResponseRedirect(f'/institute/profile/{institue_pk}')


def approvals(request,pk):
    institute_approval = Institute.objects.get(pk=pk)
    student_designation_id = Institute_levels.objects.get(institute= request.user.profile.institute,level_name='student'  )
    if request.user.profile.designation.level_name=='teacher' or request.user.profile.designation.level_name=='principal' or request.user.profile.designation.level_name=='admin':

        if request.user.profile.designation.level_name=='teacher':
            pending_users= UserProfile.objects.filter(status='pending', institute=institute_approval, designation=student_designation_id).reverse()
            parent_request_inactive= AddChild.objects.filter(status='pending', institute=request.user.profile.institute)
            parent_request_active= AddChild.objects.filter(status='active', institute=request.user.profile.institute)
            active_users= UserProfile.objects.filter(status='approve', institute=institute_approval, designation=student_designation_id).reverse()
            inactive_users= UserProfile.objects.filter(status='dissapprove', institute=institute_approval, designation=student_designation_id).reverse()
            return render(request, 'main_app/Approvals.html', {'Pending_user':pending_users,'parent_request_active':parent_request_active,'parent_request_inactive':parent_request_inactive,'Active_user':active_users,'Inactive_user':inactive_users})
        else:
            pending_users= UserProfile.objects.filter(status='pending', institute=institute_approval).order_by('id')
            active_users= UserProfile.objects.filter(status='approve', institute=institute_approval).order_by('id')
            inactive_users= UserProfile.objects.filter(status='dissapprove', institute=institute_approval).order_by('id')
        return render(request, 'main_app/Approvals.html', {'Pending_user':pending_users,'Active_user':active_users,'Inactive_user':inactive_users})
    else:
        messages.info(request, "You don't have permission to approve/disapprove requests.")
        return redirect('not_found')

def index(request):
    return HttpResponseRedirect(request, 'main_app/index.html')

@login_required
def dashboard(request):

    # random classmates
    # if request.user.profile.designation == "student":
    std_random=UserProfile.objects.filter(designation__level_name="student").order_by('?')[:5]
    print(std_random)
        

    # Events & Calendars
    holiday=HolidayList.objects.filter(institute=request.user.profile.institute,applicable="Yes")
    exam_she =ExamDetails.objects.filter(institute=request.user.profile.institute)
  
    # starting assigned teachers
    user_one = request.user
    if request.user.profile.designation == "teacher":
        teacher_class = Classes.objects.get(class_teacher= user_one)
    
    if request.user.profile.designation:

        if request.user.profile.designation.level_name == "teacher":  
                        
            teacher_class = Classes.objects.get(class_teacher= user_one)
            
            teacher_subject = Subjects.objects.filter(subject_class= teacher_class)
        else:
            
            teacher_class = None
            teacher_subject = None    
    else:

        teacher_class = None
        teacher_subject = None
       
    # starting assigned classes
    user_institute_one= request.user.profile.institute
    user_subject_one= Subjects.objects.filter(institute= user_institute_one, subject_teacher= user_one) 
        
    # class attendance status 
    
    
# starting class teacher's  class status for last six days
    last_six_days_list = []
    ct_present_status = []
    ct_absent_status = []
    ct_leave_status = []
    for i in range(0,6): # creating list of last six days
        last_six_days_list.append(datetime.date.today() - datetime.timedelta(i))

    teacher_class = Classes.objects.filter(class_teacher = request.user).first()

    for i in last_six_days_list:
        total_present_studentsc = Attendance.objects.filter(attendance_status="present" , student_class= teacher_class , date= i ).count()
        total_absent_studentsc = Attendance.objects.filter(attendance_status="absent" , student_class= teacher_class , date= i ).count()
        total_leave_studentsc = Attendance.objects.filter(attendance_status="leave" , student_class= teacher_class , date= i ).count()
        ct_present_status.append(total_present_studentsc)
        ct_absent_status.append(total_absent_studentsc)
        ct_leave_status.append(total_leave_studentsc)
    
    final_data = []
    for i,j,k,l in zip(last_six_days_list, ct_present_status, ct_absent_status, ct_leave_status):
        one_list = []
        one_list.append(i)
        one_list.append(j)
        one_list.append(k)
        one_list.append(l)
        final_data.append(one_list)
    


# ending class teacher's  class status for last six days

   

    # starting student,teacher & class count
    try:
        total_std=UserProfile.objects.filter(institute=request.user.profile.institute, designation__level_name="student", status="approve").count()
    except UserProfile.DoesNotExist:
        total_std=0
    try:
        total_teacher=UserProfile.objects.filter(institute=request.user.profile.institute, designation__level_name="teacher", status="approve").count()
    except UserProfile.DoesNotExist:
        total_teacher=0
    try:
        total_class=Classes.objects.filter(institute=request.user.profile.institute).count()
    except Classes.DoesNotExist:
        total_class=0
    # ending student,teacher & class count
    
    # Active Users Count
    time= timezone.now()- datetime.timedelta(minutes=30)
    time1= timezone.now()
    count=User.objects.filter(last_login__gte=time,last_login__lte=time1)
    
    online_user=[]
    for i_user in count:
        if i_user.profile.institute==request.user.profile.institute:
            online_user.append(i_user)

    len_online_user=len(online_user)
    
    # Approvals Data Query Start
    date=datetime.date.today()
    last1weeks=date - datetime.timedelta(weeks=1)
    last2weeks=date - datetime.timedelta(weeks=2)
    last3weeks=date - datetime.timedelta(weeks=3)
    last4weeks=date - datetime.timedelta(weeks=4)
    last5weeks=date - datetime.timedelta(weeks=5)
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now()).count()
     
    # Approvals for 5th week
    approve5=UserProfile.objects.filter(institute=request.user.profile.institute,status="approve",updated_at__date__range=[last5weeks,last4weeks]).count()
    disapprove5=Institute_disapproved_user.objects.filter(institute=request.user.profile.institute,date__range=[last5weeks,last4weeks]).count()
    pending5=UserProfile.objects.filter(institute=request.user.profile.institute,status="pending",created_at__date__range=[last5weeks,last4weeks]).count()
   
    # Aprrovals for 4th week
    approve4=UserProfile.objects.filter(institute=request.user.profile.institute,status="approve",updated_at__date__range=[last4weeks,last3weeks]).count()
    disapprove4=Institute_disapproved_user.objects.filter(institute=request.user.profile.institute,date__range=[last4weeks,last3weeks]).count()
    pending4=UserProfile.objects.filter(institute=request.user.profile.institute,status="pending",created_at__date__range=[last4weeks,last3weeks]).count()

    # Approvals for 3rd week
    approve3=UserProfile.objects.filter(institute=request.user.profile.institute,status="approve",updated_at__date__range=[last3weeks,last2weeks]).count()
    disapprove3=Institute_disapproved_user.objects.filter(institute=request.user.profile.institute,date__range=[last3weeks,last2weeks]).count()
    pending3=UserProfile.objects.filter(institute=request.user.profile.institute,status="pending",created_at__date__range=[last3weeks,last2weeks]).count()

    # Approvals for 2nd week
    approve2=UserProfile.objects.filter(institute=request.user.profile.institute,status="approve",updated_at__date__range=[last2weeks,last1weeks]).count()
    disapprove2=Institute_disapproved_user.objects.filter(institute=request.user.profile.institute,date__range=[last2weeks,last1weeks]).count()
    pending2=UserProfile.objects.filter(institute=request.user.profile.institute,status="pending",created_at__date__range=[last2weeks,last1weeks]).count()

    # Approvals for current week
    approve1=UserProfile.objects.filter(institute=request.user.profile.institute,status="approve",updated_at__date__range=[last1weeks,date]).count()
    disapprove1=Institute_disapproved_user.objects.filter(institute=request.user.profile.institute,date__range=[last1weeks,date]).count()
    pending1=UserProfile.objects.filter(institute=request.user.profile.institute,status="pending",created_at__date__range=[last1weeks,date]).count()
    
    # Total Approvals Data
    approve_data= UserProfile.objects.filter(institute=request.user.profile.institute,status="approve").count()
    disapprove_data= Institute_disapproved_user.objects.filter(institute=request.user.profile.institute).count()
    pending_data= UserProfile.objects.filter(institute=request.user.profile.institute,status="pending").count()
    # Approvals Data Query End
    
    # starting parent child data for dashboard
    parent_children = AddChild.objects.filter(parent= request.user.profile,status="active")
    
    # ending parent child data for dashboard
    if request.user.profile.institute:
        session_start_date = request.user.profile.institute.session_start_date

    # starting attendace data for dashboard
    all_classes = Classes.objects.filter(institute= request.user.profile.institute)
    for c in all_classes:
        total_student_class = UserProfile.objects.filter(institute= request.user.profile.institute, designation__level_name="student", Class= c).count()
        c.total_student = total_student_class

        present_student = Attendance.objects.filter(institute= request.user.profile.institute, attendance_status="present" , student_class= c , date=  datetime.date.today() ).count()
        c.total_present = present_student

        # fetching all absent student for class
        absent_student = Attendance.objects.filter(institute= request.user.profile.institute, attendance_status="absent", student_class = c , date = datetime.date.today() ).count()
        c.total_absent = absent_student
 
        leave_student = Attendance.objects.filter(institute= request.user.profile.institute, attendance_status="leave", student_class = c, date = datetime.date.today()).count()
        c.total_leave = leave_student
    # ending attendace data for dashboard

    # starting students attendance status
    if request.user.profile.designation:

        if request.user.profile.designation.level_name == "student":
            try:
                total_days_open = Attendance.objects.filter(student= request.user, institute= request.user.profile.institute, date__gte= request.user.profile.institute.session_start_date ).count()
                
                total_days_present= Attendance.objects.filter(student= request.user, institute= request.user.profile.institute, date__gte= request.user.profile.institute.session_start_date, attendance_status='present' ).count()
                
                total_days_absent = Attendance.objects.filter(student= request.user, institute= request.user.profile.institute, date__gte= request.user.profile.institute.session_start_date, attendance_status='absent' ).count()

                total_days_leave = Attendance.objects.filter(student= request.user, institute= request.user.profile.institute, date__gte= request.user.profile.institute.session_start_date, attendance_status='leave' ).count()
                student_attendance_percentage = (total_days_present/total_days_open)*100
                student_attendance_percentage = round(student_attendance_percentage, 2)

                request.user.student_total_days_school_open = total_days_open
                request.user.student_total_days_present = total_days_present
                request.user.student_total_days_absent = total_days_absent
                request.user.student_total_days_leave = total_days_leave
                request.user.student_attendance_percentage = student_attendance_percentage
            except:
                pass

        # ending students attendance status

    # starting user notice
    if request.user.profile.designation:
        teacher_role_level = Institute_levels.objects.get(level_name='teacher', institute= request.user.profile.institute)
        teacher_role_level = teacher_role_level.level_id
        user_role_level = request.user.profile.designation.level_id
        request.user.users_notice = []
        all_notices = Notice.objects.all().order_by('id')
        if user_role_level < teacher_role_level:
            request.user.users_notice = all_notices.exclude(category="absent").reverse()
        else:
            for notice in all_notices:
                notice_recipients = notice.recipients_list.all()
                if request.user.profile in notice_recipients:
                    request.user.users_notice.insert(0, notice)
        # ending user notice

    context = {
        'all_classes': all_classes,
       'parent_children': parent_children,
       'teacher_subject': teacher_subject,
       'user_subject_one':user_subject_one,
       'holiday':holiday, 
        'total_std':total_std,
        'total_teacher':total_teacher,
        'total_class':total_class,
        'approve_data':approve_data,
        'disapprove_data':disapprove_data,
        'pending_data':pending_data,
        'approve1':approve1,
        'disapprove1':disapprove1,
        'pending1':pending1,
        'approve2':approve2,
        'disapprove2':disapprove2,
        'pending2':pending2,
        'approve3':approve3,
        'disapprove3':disapprove3,
        'pending3':pending3,
        'approve4':approve4,
        'disapprove4':disapprove4,
        'pending4':pending4,
        'approve5':approve5,
        'disapprove5':disapprove5,
        'pending5':pending5, 
        'active_sessions':active_sessions,  
        'len_online_user':len_online_user,  
        'holiday':holiday,
        'final_data': final_data,
        'exam_she':exam_she,
        'std_random':std_random,
}
    return render(request, 'main_app/dashboard.html' , context)



class RegistrationViewUniqueEmail(RegistrationView):
    form_class = RegistrationFormUniqueEmail

def login(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
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
      # starting user notice
    if request.user.profile.designation:
        teacher_role_level = Institute_levels.objects.get(level_name='teacher', institute= request.user.profile.institute)
        teacher_role_level = teacher_role_level.level_id
        user_role_level = request.user.profile.designation.level_id
        request.user.users_notice = []
        all_notices = Notice.objects.all().order_by('id')
        if user_role_level < teacher_role_level:
            request.user.users_notice = all_notices.exclude(category="absent").reverse()
        else:
            for notice in all_notices:
                notice_recipients = notice.recipients_list.all()
                if request.user.profile in notice_recipients:
                    request.user.users_notice.insert(0, notice)
        # ending user notice
    user_permissions_changes = Tracking_permission_changes.objects.filter(institute= request.user.profile.institute, role = request.user.profile.designation).last()
    
    # Parent_childern Checkpoint Start
    parent_children = AddChild.objects.filter(parent= request.user.profile,status="active")
    
    # Secondry Institute
    institute=SecondryInstitute.objects.filter(student_name=request.user.profile,status="active")
    if user_permissions_changes:
        users_old_permissions = user_permissions_changes.old_permissions.all()
        users_new_permissions = user_permissions_changes.updated_permissions.all()
        changes_comment = user_permissions_changes.comment
        added_permissions = []
        removed_permissions = []
    
        for permission in users_old_permissions:
            if permission not in users_new_permissions:
                removed_permissions.append(permission)
    
        for permission in users_new_permissions:
            if permission not in users_old_permissions:
                added_permissions.append(permission)


        update_time = user_permissions_changes.update_time        
        context = {
        'added_permissions': added_permissions,
        'removed_permissions': removed_permissions,
        'updated_time': update_time,
        'changes_comment': changes_comment,
        'parent_children':parent_children,
        'institute':institute

        
        }
        return render(request, 'main_app/admin_user_profile.html', context )
    context={
        'parent_children':parent_children,
        'institute':institute

    }
    return render(request, 'main_app/admin_user_profile.html', context )
    
  
    
    
def fetch_levels(request):
    id = request.POST['school_id']
    levels = Institute_levels.objects.filter( institute = id)
    nlevels="<option selected disabled value=''> -- select one --</option>"
    for t in levels:
        nlevels= nlevels+ f"<option value='{t.id}' >"+str(t)+"</option>"
    return HttpResponse(nlevels)

    
# def edit_institute(request, pk):
#     edit_institute =Institute.objects.get(pk=pk)
#     return render(request, 'main_app/edit_institute.html',{'institute_info': institute_info})




    

@login_required
def edit_profile(request, pk):
    user_info = UserProfile.objects.get(pk=pk)
    all_institutes = Institute.objects.all()
    # to get all the states
    all_states = State.objects.all()
    
    # to get all the classes
    all_institute_classes = Classes.objects.filter(institute= request.user.profile.institute)
    # Store the value of current year
    current_year=datetime.date.today().year
    
    # Store the value of next year
    next_year = datetime.date.today().year+1
    
   
        
    
    # Occurence of POST method
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
            
            new_level_admin = Institute_levels.objects.create(institute=new_create_institute, level_id=1, level_name='admin')
            new_level_principal = Institute_levels.objects.create(institute=new_create_institute, level_id=2, level_name='principal')
            new_level_parent = Institute_levels.objects.create(institute=new_create_institute, level_id=3, level_name='teacher') 
            new_level_parent = Institute_levels.objects.create(institute=new_create_institute, level_id=4, level_name='parent') 
            new_level_student = Institute_levels.objects.create(institute=new_create_institute, level_id=5, level_name='student')# creating default level for admin
            role = Role_Description.objects.create(user=request.user, institute=new_create_institute, level= new_level_admin) # creating default role for admin
            user_info.designation = new_level_admin
            user_info.institute= new_create_institute
            user_info.status = 'approve'
            user_info.save()

            # sending mail to admin on registering
            send_mail('Admin Request Confirmation ',f'Hello {request.user} , Thank you for using our application.  ', 'yourcollegeportal@gmail.com',[f'{request.user.email}'], html_message=f"<h4>Hello {request.user},</h4><p>Thank you for choosing our application.</p><p> You have requested to be an admin profile so you are able to create your own institution profile.once your request is approved you will received a confirmation email.</p>School Portal<br>school_portal@gmail.com<p></p>"
            )
        
        
        user_info.first_name= request.POST['first_name']
        user_info.middle_name= request.POST['middle_name']
        user_info.last_name= request.POST['last_name']
        user_info.father_name = request.POST.get('father_name')
        user_info.mother_name = request.POST.get('mother_name')
        user_info.gender = request.POST.get('gender')
        user_info.marital_status = request.POST.get('marital_status')
        user_info.date_of_birth= request.POST['dob']
        user_info.category= request.POST.get('category_')
        user_info.aadhar_card_number = request.POST.get('adhar_number')
        user_info.qualification= request.POST.get('user_qualification')
        if not new_admin:
            user_info.status = 'pending'

        if 'user_status' in request.POST:
            if request.POST['user_status'] == "approve" or request.POST['user_status'] == 'Approve':
                user_info.status="approve"
        
        
        if 'select_school' in request.POST: # checking if new admin select box is checked and selected institute
            selected_institute_pk = request.POST['select_school']
            updated_institute = Institute.objects.get(pk=selected_institute_pk) #fetching the selected institutes list
            user_info.institute= updated_institute
        if 'user_designation' in request.POST: 
            level_id = request.POST['user_designation']
            up_level= Institute_levels.objects.get(pk=level_id) # fetching the selected level the levels list
            user_info.designation = up_level
            new_level = Role_Description.objects.create(user=request.user, institute= updated_institute, level= up_level)

        if 'student_class' in request.POST: 
            selected_class= request.POST.get('student_class')
            user_info.Class= Classes.objects.get(pk= selected_class)
        
        if 'st_roll_number' in request.POST:
            user_info.roll_number = request.POST['st_roll_number']

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
        user_info.class_current_year=current_year
        user_info.class_next_year=next_year
   
        try:
            user_info.save()
            messages.success(request, 'Profile details updated !!!')
        except:
            messages.error(request, 'Failed to update, Please fill details correctly !!!')
            
            return redirect('user_profile')

        
        
        return redirect('user_profile')
        
    return render(request, 'main_app/edit_profile.html', {'user_info':user_info, 'all_institutes':all_institutes, 'all_states':all_states,'all_institute_classes':all_institute_classes,})


  

@login_required
def institute_profile(request, pk):
# starting assigning all functionalities to admin
    admin_pk = Institute_levels.objects.get(institute= request.user.profile.institute, level_name='admin')
    
    checking_for_admin = Role_Description.objects.filter(user=request.user, institute=request.user.profile.institute, level= admin_pk ).first()


    if checking_for_admin is not None:
        all_app_functions = App_functions.objects.all()
        for function in all_app_functions:
            request.user.user_institute_role.level.permissions.add(function)
# ending assigning all functionalities to admin


    institute_data= Institute.objects.get(pk=pk)
    institute_roles = Institute_levels.objects.filter(institute=institute_data).reverse()
    institute_class = Classes.objects.filter(institute=institute_data).reverse()
    institute_subject = Subjects.objects.filter(institute=institute_data).reverse()
    designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='teacher')
    institute_teachers = UserProfile.objects.filter(institute= request.user.profile.institute, designation=designation_pk )
    # starting user permission code
    user_permissions = request.user.user_institute_role.level.permissions.all()
    add_class_permission = App_functions.objects.get(function_name='Can Add Class')
    add_subject_permission = App_functions.objects.get(function_name='Can Add Subject')
    assign_class_teacher_permission = App_functions.objects.get(function_name='Can Assign Class Teacher')
    can_edit_class_permission = App_functions.objects.get(function_name='Can Edit Class')
    can_delete_class_permission = App_functions.objects.get(function_name='Can Delete Class')
    can_edit_subject_permission = App_functions.objects.get(function_name='Can Edit Subject')
    can_delete_subject_permission = App_functions.objects.get(function_name='Can Delete Subject')

    
    # ending user permission code
    context_data = {'institute_data':institute_data, 
    'institute_roles':institute_roles,
     'institute_class':institute_class,
     'institute_subject':institute_subject,
      'all_classes':institute_class,
      'user_permissions': user_permissions,
      'add_class_permission': add_class_permission,
      'add_subject_permission':add_subject_permission,
      'institute_teachers':institute_teachers,
      'assign_class_teacher_permission':assign_class_teacher_permission,
      'can_edit_class_permission':can_edit_class_permission,
      'can_delete_class_permission':can_delete_class_permission,
      'can_edit_subject_permission':can_edit_subject_permission,
      'can_delete_subject_permission': can_delete_subject_permission
      }

    return render(request, 'main_app/institute_profile.html', context_data)
    

   
@login_required
def edit_institute(request, pk):
    edit_institute= Institute.objects.get(pk=pk)
    return render(request, 'main_app/edit_institute.html', {'edit_institute':edit_institute})
   

class InstituteUpdateview(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Institute
    
    form_class = InstituteUpdateProfile

    template_name="main_app/edit_institute.html"
    success_message = "Details were updated successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        if self.request.user.profile.designation.level_name == "admin" or self.request.user.profile.designation.level_name == "principal":
            return True
        else:
            return False


    def get_success_url(self, **kwargs):         
        return reverse_lazy("institute_detail", kwargs={'pk':self.request.user.profile.institute.id})



def approve_request(request,pk):
    

    user = UserProfile.objects.get(pk=pk)
    user.approve()
    send_mail('Account Approved ',f'Hello {user.first_name} , Thank you for choosing our application.  ', 'yourcollegeportal@gmail.com',[f'{user.user.email}'], html_message=f"<h4>Hello {user.first_name},</h4><p>Your request to join {user.institute} as {user.designation} has been approved. Now you can login to your dashboard and update your profile.</p>School portal<br>school_portal@gmail.com<p></p>"
            )
    rr= request.user.profile.institute.id
    return HttpResponseRedirect(f'/user/approvals/{rr}/')
    

def disapprove_request(request,pk):
    user = UserProfile.objects.get(pk=pk)
    
    Institute_disapproved_user.objects.create(institute = request.user.profile.institute, user = user, applied_role = user.designation,date=datetime.date.today())
    user.designation = None #user_designation set to null
    user.institute = None # user_institute set to null
    
    disapproved_user_role_description = Role_Description.objects.get(user = user.user)
    disapproved_user_role_description.delete()

    user.disapprove()
    user.status= 'Pending'
    

    user.save()
    rr= request.user.profile.institute.id
    return HttpResponseRedirect(f'/user/approvals/{rr}/')
    

def add_new_role(request, pk):
    if request.method== "POST":
        institute = Institute.objects.get(pk=pk)
    
        new_role = Institute_levels()
        new_role.institute= institute
        new_role.level_id = request.POST['level_id']
        new_role.level_name = request.POST['level_name']
        new_role.created_by = request.user
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
    if user_role.level_name == 'admin'  or user_role.level_name == 'parent' or user_role.level_name == 'student' or user_role.level_name == 'teacher' or user_role.level_name == 'principal' :
        messages.error(request, 'Admin, principal,  teacher, Parent or student roles can not be deleted !!!')
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


def selecting_class(request):
    if request.method == 'POST':
        selected_class= request.POST.get('student_class')
        student = UserProfile.objects.get(user = request.user)
        student.Class= Classes.objects.get(pk= selected_class)
        student.save()

    return redirect('user_profile')

def assign_class_teacher(request, pk):
    user_permissions = request.user.user_institute_role.level.permissions.all()
    assign_class_teacher_permission = App_functions.objects.get(function_name='Can Assign Class Teacher')

    if assign_class_teacher_permission in user_permissions:
        selected_class = Classes.objects.get(pk=pk)
        designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='teacher')
        institute_teachers = UserProfile.objects.filter(institute= request.user.profile.institute, designation=designation_pk )
        context_data= {'selected_class':selected_class, 'institute_teachers':institute_teachers}

        if request.method == 'POST':
            new_class_teacher = request.POST.get('class_teacher')
            selected_class.class_teacher = User.objects.get(pk= new_class_teacher)
            try:
                selected_class.save()
                messages.success(request, 'Class Teacher assigned successfully!!!')
            except:
                messages.error(request,'Something went wrong !!!')

        return render(request, 'main_app/assign_class_teacher.html', context_data)
    else:
        messages.info(request, "You Don't have permission to assign Class Teacher")
        return redirect('not_found')

def not_found_page(request):
    return render(request, 'main_app/404.html')

class Edit_Role_Permissions(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Institute_levels
    fields = ['permissions']
    template_name = "main_app/role_permissions_edit.html"
    success_message = "Role Permissions Updated Successfully"
    def get_success_url(self, **kwargs):         
        return reverse_lazy("institute_detail", kwargs={'pk':self.request.user.profile.institute.id})

    

def edit_role_permissions(request, pk):
    role_to_update_permissions = Institute_levels.objects.get(pk=pk)
    roles_to_update_all_permissions = role_to_update_permissions.permissions.all()
    all_app_functions = App_functions.objects.all()
    
    user_permissions = request.user.user_institute_role.level.permissions.all()
    can_edit_role_permissions_permission = App_functions.objects.get(function_name='Can Edit Role Permissions')

    if can_edit_role_permissions_permission in user_permissions:

        if request.method == "POST":
            # creating object to to track changes in table
            tracking_permission_change = Tracking_permission_changes()
            tracking_permission_change.update_time = timezone.now()
            tracking_permission_change.changes_made_by = request.user
            tracking_permission_change.institute = request.user.profile.institute
            tracking_permission_change.role = role_to_update_permissions
            tracking_permission_change.comment = request.POST['pc_comment']
            tracking_permission_change.save()
            for old_permission in roles_to_update_all_permissions:
                tracking_permission_change.old_permissions.add(old_permission)
        

            updated_permissions = request.POST.getlist('new_permissions')
            role_to_update_permissions.permissions.clear()
            for permission in updated_permissions:
                get_permission = App_functions.objects.get(pk = permission)
                role_to_update_permissions.permissions.add(get_permission)
            for updated_permissions in updated_permissions:

                tracking_permission_change.updated_permissions.add(updated_permissions)
            messages.success(request, 'Role Permissions Updated !!!')    
            rr= request.user.profile.institute.id
            return HttpResponseRedirect(f'/institute/profile/{rr}/')
            
        context= {
            'role_to_update_permissions': role_to_update_permissions,
            'roles_all_permissions': roles_to_update_all_permissions,
            'all_app_functions':all_app_functions
        }
        return render(request, 'main_app/role_permissions_edit.html', context)
    else:
        messages.info(request, "You Don't have permission to edit permissions")
        return redirect('not_found')


class Permission_Updates_History_list_View(LoginRequiredMixin, ListView):
    
    
    template_name = 'main_app/permissions_update_history.html'
    paginate_by = 15

    def get_queryset(self):
        admin_role = Institute_levels.objects.get(institute=self.request.user.profile.institute, level_name="admin") ##skipping admin role changes
        queryset = Tracking_permission_changes.objects.filter(institute= self.request.user.profile.institute).exclude(role= admin_role).order_by('-update_time')
       
        return queryset

def fetch_classes(request):
    instiute_id = Institute.objects.get(pk=request.POST.get('school_id'))
    institute_all_classes = Classes.objects.filter(institute=instiute_id)
    all_classes = "<option selected disabled value=''> -- select your class -- </option>"
    for c in institute_all_classes:
        all_classes= all_classes+ f"<option value='{c.id}' >"+str(c)+"</option>"
    return HttpResponse(all_classes)
