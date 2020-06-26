from django.urls import path, include
from django.http import HttpResponse

from . import views
from .views import userData

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('userdata/', userData.as_view(), name="userdata_api"),
  


]