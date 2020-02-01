from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
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





# Create your views here.

def add_classes(request):
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


class ClassUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
 model = Classes
 form_class = ClassUpdateForm
 template_name="main_app/edit_class.html"
 success_message = "Details were updated successfully !!!"
 

 def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
 def get_success_url(self, **kwargs):         
        return reverse_lazy("institute_detail", kwargs={'pk':self.request.user.profile.institute.id})


# Add Subjects

def add_subjects(request):
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
 

    if request.method == 'POST':
        # class_id = request.POST.get('new_class')
        
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

        # 'all_classes':institute_classes,
        'class_info': class_to_edit,
        'institute_teachers':institute_teachers
    }
    return render(request, 'main_app/edit_class.html', context)

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
    if request.user.profile.designation.level_name=='teacher':
         pending_users= UserProfile.objects.filter(status='pending', institute=institute_approval, designation=student_designation_id)
         active_users= UserProfile.objects.filter(status='approve', institute=institute_approval, designation=student_designation_id)
         inactive_users= UserProfile.objects.filter(status='dissapprove', institute=institute_approval, designation=student_designation_id)


    else:
        pending_users= UserProfile.objects.filter(status='pending', institute=institute_approval)
        active_users= UserProfile.objects.filter(status='approve', institute=institute_approval)
        inactive_users= UserProfile.objects.filter(status='dissapprove', institute=institute_approval)

   
    return render(request, 'main_app/Approvals.html', {'Pending_user':pending_users,'Active_user':active_users,'Inactive_user':inactive_users})

def index(request):
    return HttpResponseRedirect(request, 'main_app/index.html')

@login_required
def dashboard(request):
    return render(request, 'main_app/dashboard.html')



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
    user_permissions_changes = Tracking_permission_changes.objects.filter(institute= request.user.profile.institute, role = request.user.profile.designation).last()

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
        'changes_comment': changes_comment
        
        }
        return render(request, 'main_app/admin_user_profile.html', context )
    
    return render(request, 'main_app/admin_user_profile.html' )
    
  
    
    
def fetch_levels(request):
    id = request.POST['school_id']
    levels = Institute_levels.objects.filter( institute = id)
    nlevels=""
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
    all_states = State.objects.all()
    all_institute_classes = Classes.objects.filter(institute= request.user.profile.institute)
    
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
            new_level_parent = Institute_levels.objects.create(institute=new_create_institute, level_id=2, level_name='teacher') 
            new_level_parent = Institute_levels.objects.create(institute=new_create_institute, level_id=3, level_name='parent') 
            new_level_student = Institute_levels.objects.create(institute=new_create_institute, level_id=4, level_name='student')# creating default level for admin
            role = Role_Description.objects.create(user=request.user, institute=new_create_institute, level= new_level_admin) # creating default role for admin
            user_info.designation = new_level_admin
            user_info.institute= new_create_institute
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
        if 'select_school' in request.POST: # checking if new admin select box is checked and selected institute
            selected_institute_pk = request.POST['select_school']
            updated_institute = Institute.objects.get(pk=selected_institute_pk) #fetching the selected institutes list
            user_info.institute= updated_institute
        if 'user_designation' in request.POST: 
            level_id = request.POST['user_designation']
            up_level= Institute_levels.objects.get(pk=level_id) # fetching the selected level the levels list
            user_info.designation = up_level
            new_level = Role_Description.objects.create(user=request.user, institute= updated_institute, level= up_level  )

        if 'student_class' in request.POST: 
            selected_class= request.POST.get('student_class')
            user_info.Class= Classes.objects.get(pk= selected_class)

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
        
        try:
            user_info.save()
            messages.success(request, 'Profile details updated !!!')
        except:
            messages.error(request, 'Failed to update, Please fill details correctly !!!')
            
            return redirect('user_profile')

        
        
        return redirect('user_profile')
        
    return render(request, 'main_app/edit_profile.html', {'user_info':user_info, 'all_institutes':all_institutes, 'all_states':all_states,'all_institute_classes':all_institute_classes})


  

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
  # return render(request, 'main_app/institute_profile.html', {'institute_data':institute_data, 'institute_roles':institute_roles, 'institute_class':institute_class, 'all_classes':all_classes})
    designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='teacher')
    institute_teachers = UserProfile.objects.filter(institute= request.user.profile.institute, designation=designation_pk )
    institute_subject = Subjects.objects.filter(institute=institute_data).reverse()
 
 
    context_data = {'institute_data':institute_data, 'institute_roles':institute_roles, 'institute_class':institute_class,'institute_subject':institute_subject, 'all_classes':institute_class, 'institute_teachers':institute_teachers}

    # institute_subject = Subjects.objects.filter(institute=institute_data).reverse()
    # context_data = {'institute_data':institute_data, 
    # 'institute_roles':institute_roles,
    #  'institute_class':institute_class,
    #  'institute_subject':institute_subject,
    #   'all_classes':institute_class}

    return render(request, 'main_app/institute_profile.html', context_data)
   
@login_required
def edit_institute(request, pk):
    edit_institute= Institute.objects.get(pk=pk)
    return render(request, 'main_app/edit_institute.html', {'edit_institute':edit_institute})
   

class InstituteUpdateview(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Institute
    
    form_class = InstituteUpdateProfile

    template_name="main_app/edit_institute.html"
    success_message = "Details were updated successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
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
    user.disapprove()
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
    if user_role.level_name == 'admin'  or user_role.level_name == 'parent' or user_role.level_name == 'student' or user_role.level_name == 'teacher'  :
        messages.error(request, 'Admin, teacher, Parent or student roles can not be deleted !!!')
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


class Permission_Updates_History_list_View(LoginRequiredMixin, ListView):
    
    
    template_name = 'main_app/permissions_update_history.html'
    paginate_by = 15

    def get_queryset(self):
        admin_role = Institute_levels.objects.get(institute=self.request.user.profile.institute, level_name="admin") ##skipping admin role changes
        queryset = Tracking_permission_changes.objects.filter(institute= self.request.user.profile.institute).exclude(role= admin_role).order_by('-update_time')
       
        return queryset
