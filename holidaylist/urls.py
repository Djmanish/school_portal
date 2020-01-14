from django.urls import path, include
from django.http import HttpResponse

from . import views
from .views import holidaylist,HolidayUpdateView,emailView,successView

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('holiday/<int:pk>', views.holidaylist, name="holidaylist"),
  path('holiday/delete/<int:pk>', views.delete_holiday,name='delete_holiday'),
  path('holiday/edit/<int:pk>/',views.edit_holiday, name='edit_holiday'),
  path('mails/<int:pk>/', views.emailView, name='emailView'),
 
  path('success/', views.successView, name='successView')


]
