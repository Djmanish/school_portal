from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.urls import reverse_lazy, reverse
from django.views.generic import *
from django.contrib.messages.views import SuccessMessageMixin

from django.http import HttpResponseRedirect
from django.urls import reverse
from holidaylist import templates
from django.contrib import messages
from holidaylist.models import *
from main_app import models

from main_app import urls
from holidaylist.urls import *
from holidaylist.forms import ContactForm
from django.core.mail import send_mail, send_mass_mail, mail_admins, mail_managers



        # Create your views here.
def holidaylist(request):
    institute_holiday_list = HolidayList.objects.all()
    if request.method == "POST":
                holiday_date= request.POST.get('holiday_date')
                holiday_day= request.POST.get('holiday_day')
                holiday_name= request.POST.get('holiday_name')

                holiday_applicable= request.POST.get('holiday_applicable')
                holiday_type= request.POST.get('holiday_type')
                holiday_email_send= request.POST.get('holiday_email_send')

                holiday_sms_send= request.POST.get('holiday_sms_send')
                holiday_notification_send= request.POST.get('holiday_notification_send')

                new_holiday = HolidayList.objects.create(date=holiday_date, days= holiday_day, name= holiday_name, applicable=holiday_applicable,holiday_type=holiday_type, holiday_email=holiday_email_send, holiday_sms=holiday_sms_send, holiday_notification=holiday_notification_send )
        
                messages.success(request, 'New Holiday Created successfully !!!')
    

    return render(request, 'holidaylist/holidaylist.html',{'institute_holiday_list':institute_holiday_list})


                
def edit_holiday(request, pk):
    edit_holiday= HolidayList.objects.get(pk=pk)
    return render(request, 'holidaylist/edit_holiday.html', {'edit_holiday':edit_holiday})
   
from .forms import HolidayUpdateForm
class HolidayUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
 model = HolidayList
 form_class = HolidayUpdateForm
 template_name="holidaylist/edit_holiday.html"
 success_message = "Details were updated successfully"
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

def emailView(request):
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
            return redirect('holidaylist')
    return render(request, "holidaylist/holiday_email.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')