from django.shortcuts import render, HttpResponseRedirect
from holidaylist import templates
from holidaylist.models import *
from main_app import models
from main_app import views
from main_app import urls

# Create your views here.

    
# def add_holiday(request):
#         if request.method == "POST":
#             holiday_date= request.POST['holiday_date']
#             holiday_day= request.POST['holiday_day']
#             holiday_name= request.POST['holiday_name']

#             holiday_applicable= request.POST['holiday_applicable']
#             holiday_type= request.POST['holiday_type']
#             holiday_email_send= request.POST['holiday_email_send']

#             holiday_sms_send= request.POST['holiday_sms_send']
#             holiday_notification_send= request.POST['holiday_notification_send']

#             holiday_list = HolidayList.objects.create(date=holiday_date, days= holiday_day, name= holiday_name, applicable=holiday_applicable,holiday_type=holiday_type, holiday_email=holiday_email_send, holiday_sms=holiday_sms_end, holiday_notification=holiday_notification_send )

#             messages.success(request, 'New Holiday Created successfully !!!')
#     return render(request, 'holidaylist/holidaylist.html')
            
          # return HttpResponseRedirect(f'/institute/holidaylist/data')

def holidaylist(request):
    institute_holiday_list = HolidayList.objects.all()
    return render(request, 'holidaylist/holidaylist.html',{'institute_holiday_list':institute_holiday_list})
  
