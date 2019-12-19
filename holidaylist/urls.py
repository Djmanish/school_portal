from django.urls import path, include
from main_app.urls import *

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('/institute/holidaylist/data', views.holidaylist, name="holidaylist_data")
  path('/institute/holidaylist/', views.add_holiday, name="holidaylist")


]
