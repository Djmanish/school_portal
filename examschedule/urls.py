from django.urls import path, include
from django.http import HttpResponse

from . import views
from .views import MemberList

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('examschedule/<int:pk>', MemberList.as_view(), name="examschedule"),
 


]
