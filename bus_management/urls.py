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
  path('fetch_bus_details/', views.fetch_bus_details, name="fetch_bus_details"),
  path('fetch_point_details/', views.fetch_point_details, name="fetch_point_details"),
  path('fetch_driver_details/', views.fetch_driver_details, name="fetch_driver_details"),
  path('add_driver/', views.add_driver, name="add_driver"),
  path('add_new_driver/', views.add_new_driver, name="add_new_driver"),
  path('add_route/', views.add_route, name="add_route"),
  path('edit_route/', views.edit_route, name="edit_route"),
  path('delete_route/<int:pk>/',views.delete_route,name='delete_route'),
  path('route_map/', views.route_map, name="route_map"),
  path('add_point_route/',views.add_point_route, name="add_point_route"),
  path('set_location/', views.set_location, name="set_location"),
  path('see_map/', views.see_map, name="see_map"),
  path('update_map_route/', views.update_map_route, name="update_map_route"),
  path('delete_routemap/<int:pk>/',views.delete_routemap,name='delete_routemap'),
  path('update_route/', views.update_route, name="update_route"),
  path('view_routepoints/<int:pk>', views.view_routepoints, name="view_routepoints"),
  path('update_routepoints/', views.update_routepoints, name="update_routepoints"),
  path('view_delete_view_routepoints/<int:pk>', views.delete_view_routepoints, name="delete_view_routepoints"),
  path('start_trip/<int:pk>/', views.start_trip, name="start_trip"),
  path('add_trip/', views.add_trip, name="add_trip"),
]
