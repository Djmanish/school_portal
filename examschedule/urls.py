from django.urls import path, include
from django.http import HttpResponse

from . import views
from .views import examschedule

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('examschedule/<int:pk>', views.examschedule, name="examschedule"),
  path('update_examschedule/<int:pk>', views.update_examschedule, name='update_examschedule'),
 


]
