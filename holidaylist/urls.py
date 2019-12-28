from django.urls import path, include

from . import views
from .views import holidaylist,HolidayUpdateView

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('', views.holidaylist, name="holidaylist"),
  # path('holidays/add/', views.add_holiday, name="add_holiday")
  path('holiday/edit/<int:pk>/',HolidayUpdateView.as_view(), name='edit_holiday')


]
