from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView




urlpatterns = [
    path('',views.attendance ,name='attendance'),
    path('attendanceupdate/<int:pk>/',views.attendance_update ,name='attendanceupdate'),
    

  


]
