from django.urls import path, include
from django.http import HttpResponse

from . import views
from .views import exam_schedule

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('examschedule/<int:pk>', views.exam_schedule, name="examschedule"),
  path('create_examschedule/<int:pk>', views.create_exam_schedule, name="create_examschedule"),
  # path('examtypelist/<int:pk>',views.exam_type, name="create_test_type"),
  path('examschedule/view/<int:pk>', views.examschedule_view, name='examschedule_view'),
  path('examtypelist/<int:pk>', views.create_test_type, name="create_test_type"),
  path('fetching_max_sr_no/', views.fetch_max_sr_no, name='fetch_max_sr_no' ),
  path('fetching_no/', views.fetch_no, name='fetch_no' ),

  path('selected_exam_type/', views.selected_exam_type, name='selected_exam_type' ),
  path('examtypelist/edit/<int:pk>/', views.edit_test_type, name='edit_test_type'),
  path('examtypelist/delete/<int:pk>/', views.delete_test_type, name='delete_test_type'),
  path('examschedule/edit/<int:pk>/', views.edit_examschedule, name='edit_examschedule'),
  path('examschedule/delete/<int:pk>/', views.delete_examschedule, name='delete_examschedule'),

 


]
