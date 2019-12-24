from django.urls import path, include
from main_app.urls import *

from holidaylist import views

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('holidaylist/', views.holidaylist, name="holidaylist"),
  path('holidays/add', views.add_holiday, name="add_holiday")


]
