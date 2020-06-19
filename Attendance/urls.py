from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView




urlpatterns = [
    path('',views.attendance ,name='attendance'),
    # path('attendance_principal',views.attendance_principal ,name='attendance_principal'),
    path('attendanceupdate/<int:pk>/',views.attendance_update ,name='attendanceupdate'),
    path('update_attendance_record/<int:pk>/', views.update_attendance_record, name="update_attendace_record"),
    path('attendance_status_current/<int:pk>/', views.current_date_attendance_record, name="current_attendance_record"),
    path('students_list/', views.class_students_list, name="class_students_list"),
    path('student_detail/<int:pk>/', views.student_detail, name="student_detail"),
  
    

  


]
