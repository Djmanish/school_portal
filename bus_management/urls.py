from django.urls import path, include
from django.http import HttpResponse

from . import views
from .views import *

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('create_route/<int:pk>', views.exam_result, name="examresult"),

  


  path('result/', views.st_result, name="st_result")
 
              ]
