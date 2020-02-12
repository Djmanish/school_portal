from django.urls import path, include
from django.http import HttpResponse

from . import views
from .views import exam_schedule

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('examschedule/<int:pk>', views.exam_schedule, name="examschedule"),
  # path('examtypelist/<int:pk>',views.exam_type, name="create_test_type"),
  path('examschedule/view/<int:pk>', views.examschedule_view, name='examschedule_view'),
  path('examtypelist/<int:pk>', views.create_test_type, name="create_test_type")

 


]
