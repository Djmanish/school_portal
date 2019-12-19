from django.shortcuts import render, HttpResponseRedirect
from holidaylist import templates
from holidaylist.models import *
from main_app.models import *
from main_app.views import *
from main_app.urls import *

# Create your views here.

    
def add_holiday(request):
        if request.method == "POST":
            holiday_date= request.POST['holiday_date']
            holiday_day= request.POST['holiday_day']
            holiday_name= request.POST['holiday_name']

            holiday_applicable= request.POST['holiday_applicable']
            holiday_type= request.POST['holiday_type']
            holiday_email_send= request.POST['holiday_email_send']

            holiday_sms_send= request.POST['holiday_sms_send']
            holiday_notification_send= request.POST['holiday_notification_send']




            # rr=request.user.profile.institute.id

            # holiday_day=DAYS_OF_WEEK.objects.get(id=holiday_day)

            holiday_list = HolidayList.objects.create(institute=request.user.profile.institute, holiday_date=holiday_date, holiday_day= holiday_day, holiday_name= holiday_name, holiday_applicable=holiday_applicable,holiday_type=holiday_type, holiday_email_send=holiday_email_send, holiday_sms_end=holiday_sms_end, holiday_notification_send=holiday_notification_send )

            messages.success(request, 'New Holiday Created successfully !!!')
            
          return HttpResponseRedirect(f'/institute/holidaylist/data')

def holidaylist(request, pk):
    institute_data= Institute.objects.get(pk=pk)
    institute_holiday_list = HolidayList.objects.filter(institute=institute_data).reverse()
    return render(request, 'holidaylist/holidaylist.html',{'institute_holiday_list': institute_holiday_list})
   
