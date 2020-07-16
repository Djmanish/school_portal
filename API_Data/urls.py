from django.urls import path, include
from django.http import HttpResponse

from . import views
from .models import *
from .views import RegisterView, VerifyEmail


# from holidaylist.views import add_holiday




urlpatterns = [
  
  # path('userdata/', userData.as_view(), name="userdata_api"),
  path('task-list/', views.tasklist, name="userdata_api"),
  path('task-detail/<str:pk>/', views.taskDetail, name="task-detail"),
  path('task-create/', views.taskCreate, name="task-create"),

  path('register/', RegisterView.as_view(), name="register"),
  path('email-verify/', VerifyEmail.as_view(), name="email-verify"),


  
  


]