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
  path('del_bus/<int:pk>/',views.del_bus,name='del_bus'),
]
