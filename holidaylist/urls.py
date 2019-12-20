from django.urls import path, include
from main_app.urls import *
from main_app.views import *

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('institute/holidaylist/data/', views.holidaylist, name="holidaylist")
  # path('', views.add_holiday, name="holidaylist")


]
