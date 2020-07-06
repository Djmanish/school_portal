from django.urls import path, include
from django.http import HttpResponse

from . import views
# from .views import userData


# from holidaylist.views import add_holiday




urlpatterns = [
  
  # path('userdata/', userData.as_view(), name="userdata_api"),
  path('task-list/', views.tasklist, name="userdata_api"),
  path('task-detail/<str:pk>/', views.taskDetail, name="task-detail"),
  path('task-create/', views.taskCreate, name="task-create"),
  
  


]