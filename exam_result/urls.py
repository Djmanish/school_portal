from django.urls import path, include
from django.http import HttpResponse

from . import views
from .views import exam_result,exam_view

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('examresult/<int:pk>', views.exam_result, name="examresult"),
  path('examview/<int:pk>',views.exam_view, name="examview"),
  path('studentview/<int:pk>', views.student_view, name="studentview"),
  
 
 


]
