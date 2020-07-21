from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.urls import reverse_lazy, reverse
from django.views.generic import *
from django.contrib.messages.views import SuccessMessageMixin

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from holidaylist import templates
from django.contrib import messages
from holidaylist.models import *
from main_app.models import *
from django.views.generic.edit import DeleteView
from main_app import urls
from holidaylist.urls import *
from holidaylist.forms import ContactForm
from django.core.mail import send_mail, send_mass_mail, mail_admins, mail_managers
from notices.models import *
from django.utils import timezone
from django.core.exceptions import PermissionDenied




        # Create your views here.
def holidaylist(request,pk):
        # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice

    inst = request.user.profile.institute.id

    if pk==inst:
        
            institute_holiday = Institute.objects.get(pk=pk)
            institute_holiday_list = HolidayList.objects.filter(institute=institute_holiday)
            user_permissions = request.user.user_institute_role.level.permissions.all()
            can_add_holiday_permission = App_functions.objects.get(function_name='Can Add Holiday')

            if request.method == "POST":
                if can_add_holiday_permission in user_permissions:
                        holiday_date= request.POST.get('holiday_date')
                        
                        holiday_name= request.POST.get('holiday_name')

                        holiday_applicable= request.POST.get('holiday_applicable')
                        holiday_type= request.POST.get('holiday_type')
                        holiday_email_send= request.POST.get('holiday_email_send')

                        holiday_sms_send= request.POST.get('holiday_sms_send')
                        holiday_notification_send= request.POST.get('holiday_notification_send')
                    
                        new_holiday = HolidayList.objects.create(institute=request.user.profile.institute, date=holiday_date,  name= holiday_name, applicable=holiday_applicable,holiday_type=holiday_type, holiday_email=holiday_email_send, holiday_sms=holiday_sms_send, holiday_notification=holiday_notification_send )
                
                        messages.success(request, 'New holiday created successfully !')
                    
                        # institute_holidaylist = HolidayList.objects.filter(institute=institute_holiday).reverse()
            
            user_permissions = request.user.user_institute_role.level.permissions.all()
            can_add_holiday_permission = App_functions.objects.get(function_name='Can Add Holiday')
            can_edit_holiday_permission = App_functions.objects.get(function_name='Can Edit Holiday')
            can_delete_holiday_permission = App_functions.objects.get(function_name='Can Delete Holiday')

            context = {'institute_holiday_list':institute_holiday_list,
            'user_permissions': user_permissions,
            'can_add_holiday_permission':can_add_holiday_permission,
            'can_edit_holiday_permission':can_edit_holiday_permission,
            'can_delete_holiday_permission': can_delete_holiday_permission


            }
            return render(request, 'holidaylist/holidaylist.html', context)

            

    else:
        raise PermissionDenied
                
def edit_holiday(request, pk):
        # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
    edit_holiday= HolidayList.objects.get(pk=pk)
    user_permissions = request.user.user_institute_role.level.permissions.all()
    can_edit_holiday_permission = App_functions.objects.get(function_name='Can Edit Holiday')

    
    if request.method == 'POST':
        if can_edit_holiday_permission in user_permissions:


            holiday_date=request.POST.get('holiday_date') 
            
            holiday_name =  request.POST.get('holiday_name')
            holiday_applicable =  request.POST.get('holiday_applicable')
            holiday_type =  request.POST.get('holiday_type')
            holiday_email =  request.POST.get('holiday_email')
            holiday_sms =  request.POST.get('holiday_sms')
            holiday_notification =  request.POST.get('holiday_notification')

            edit_holiday.date=holiday_date
           
            edit_holiday.name=holiday_name
            edit_holiday.applicable=holiday_applicable
            edit_holiday.holiday_type=holiday_type
            edit_holiday.holiday_email=holiday_email
            edit_holiday.holiday_sms=holiday_sms
            edit_holiday.holiday_notification=holiday_notification

            edit_holiday.save()
            messages.success(request, 'Holiday updated successfully !')
            rr=request.user.profile.institute.pk
            return HttpResponseRedirect(f'/holiday/holiday/{rr}')
        else:
            messages.info(request, "You don't have permission to edit holiday info !")
            return redirect('not_found')

    return render(request, 'holidaylist/edit_holiday.html', {'edit_holiday':edit_holiday})


def delete_holiday(request,pk):
        # starting user notice
         if request.user.profile.designation:
            request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice


         delete_holiday=HolidayList.objects.get(pk=pk)
         delete_holiday.date="null"
         delete_holiday.days="null"
         delete_holiday.name="null"
         delete_holiday.applicable="null"
         delete_holiday.holiday_type="null"
         delete_holiday.holiday_email="null"
         delete_holiday.holiday_sms="null"
         delete_holiday.holiday_notification="null"
         delete_holiday.delete()
         messages.success(request, 'Holiday deleted successfully !')
         rr=request.user.profile.institute.pk
         return HttpResponseRedirect(f'/holiday/holiday/{rr}')



from .forms import HolidayUpdateForm

class HolidayUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

 model = HolidayList
 form_class = HolidayUpdateForm
 template_name="holidaylist/edit_holiday.html"
 success_message = "Details were updated successfully !"
 success_url= "/holiday"

def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


def holidayemail(request):
        return render('holidaylist/holiday_email.html')

# def send_mails(request):
#     holiday_email = SendEmail.objects.all()
#  return render('holidaylist/holiday_email.html',{'holiday_email':holiday_email})

#         # mail= send_mail("Test", "Hello",'yourcollegeportal@gmail.com',['neha.gautam869@gmail.com'], fail_silently=False, html_message="Test")

#         # if mail:
#         #    return HttpResponse(mail)
#         # else :
#         #    raise Exception("Error")

def emailView(request,pk):
        # starting user notice
    if request.user.profile.designation:
        request.user.users_notice = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now(), recipients_list = request.user.profile).order_by('id').reverse()[:10]
    # ending user notice
    institute_holiday = Institute.objects.get(pk=pk)
    # user_emails=UserProfile.objects.filter(institute=request.user.profile.institute)
    # user_data_email=[]
    # for user_data in user_emails:
    #     user_data_email.append(user_data.user.email)
    

    institute_holiday_list = HolidayList.objects.filter(institute=institute_holiday)
    
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data['to_email']
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            
            try:
                send_mail(subject, message,from_email,[to_email],fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            
            return render(request, 'holidaylist/holidaylist.html',{'institute_holiday_list':institute_holiday_list})
    
    context={
        # 'user_data_email':user_data_email,
        'form': form,
        'institute_holiday_list':institute_holiday_list
    }        
    return render(request, "holidaylist/holiday_email.html", context)

def successView(request):
    return HttpResponse('Success! Thank you for your message.')