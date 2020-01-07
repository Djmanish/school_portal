from django.urls import path, include
from django.http import HttpResponse

from . import views
from .views import holidaylist,HolidayUpdateView,emailView,successView

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('holiday/<int:pk>', views.holidaylist, name="holidaylist"),
 
  path('holiday/edit/<int:pk>/',HolidayUpdateView.as_view(), name='edit_holiday'),
  path('mails/<int:pk>/', views.emailView, name='emailView'),
 
  path('success/', views.successView, name='successView')


]
