from django.urls import path, include
from django.http import HttpResponse

from . import views
from .views import *

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('examresult/<int:pk>', views.exam_result, name="examresult"),
  path('studentview/<int:pk>', views.student_view, name="studentview"),
  path('fetching_sr_no/', views.fetch_sr_no, name='fetch_result_sr_no' ),
  path('report_card/<int:pk>',views.report_card, name='report_card'),


  
 
 


]
