from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView




urlpatterns = [
    path('',views.attendance ,name='attendance'),
    # path('attendance_principal',views.attendance_principal ,name='attendance_principal'),
    path('attendanceupdate/<int:pk>/',views.attendance_update ,name='attendanceupdate'),
    
    

  


]
