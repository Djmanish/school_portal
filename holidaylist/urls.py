from django.urls import path, include
from django.http import HttpResponse

from . import views
from .views import holidaylist,HolidayUpdateView,send_mails

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('', views.holidaylist, name="holidaylist"),
  # path('holidays/add/', views.add_holiday, name="add_holiday")
  path('holiday/edit/<int:pk>/',HolidayUpdateView.as_view(), name='edit_holiday'),
  path('mails/', views.send_mails, name='send_mails')
  # path('holidayemail/', views.holiday_email,name='holidayemail')


]
