from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import *

from django.http import HttpResponseRedirect
from django.urls import reverse
from holidaylist import templates
from django.contrib import messages
from holidaylist.models import *
from main_app import models
from main_app import views
from main_app import urls
from holidaylist.urls import *



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

        
# def add_holiday(request):
   

       
     
     
#         return HttpResponseRedirect(f'/holidaylist/holidaylist/')
                

class HolidayUpdateView(UpdateView):
 model = HolidayList
 fields = ['date','days','name', 'applicable','holiday_type','holiday_email','holiday_sms','holiday_notification']

 template_name="holidaylist/holidaylist.html"
 success_message = "Details were updated successfully"
