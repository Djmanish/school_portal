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
  path('add_driver/', views.add_driver, name="add_driver"),
  path('add_new_driver/', views.add_new_driver, name="add_new_driver"),
  path('add_route/', views.add_route, name="add_route"),
  path('route_map/', views.route_map, name="route_map"),
  path('add_point_route/',views.add_point_route, name="add_point_route"),
  path('set_location/', views.set_location, name="set_location"),
  path('see_map/', views.see_map, name="see_map"),

]
