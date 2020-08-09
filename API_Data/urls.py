from django.urls import path, include
from django.http import HttpResponse

from . import views
from .models import *
from .views import * 

# from holidaylist.views import add_holiday




urlpatterns = [
  
  # path('userdata/', userData.as_view(), name="userdata_api"),
  path('task-list/', views.tasklist, name="userdata_api"),
  path('task-detail/<str:pk>/', views.taskDetail, name="task-detail"),
  path('task-create/', views.taskCreate, name="task-create"),

  path('login/',LoginAPIView.as_view(), name="login"),
  path('registration/', RegisterView.as_view(), name="registration"),
  # path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
  path('request-reset-email/', RequestPasswordResetEmail.as_view(),name="request-reset-email"),
  path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
  path('userprofile/',UserProfileViews.as_view(), name="userprofile"),



  
  


]