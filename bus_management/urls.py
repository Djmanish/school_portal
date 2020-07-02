from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView
from django.conf.urls import url

# from holidaylist.views import add_holiday




urlpatterns = [
  path('',views.bus,name='bus'),
  path('add_bus',views.add_bus,name='add_bus'),
  path('add_point',views.add_point,name='add_point'),
  path('edit_bus',views.edit_bus,name='edit_bus'),
  path('edit_point',views.edit_point,name='edit_point'),
  path('delete_point/<int:pk>/',views.delete_point,name='delete_point'),
  path('fetch_bus_details/', views.fetch_bus_details, name="fetch_bus_details"),
]
