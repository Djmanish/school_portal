from django.urls import path, include
from django.http import HttpResponse

from . import views
from .views import exam_schedule

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('examschedule/<int:pk>', views.exam_schedule, name="examschedule"),
 


]
