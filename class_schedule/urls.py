
from django.urls import path, include
from . import views




urlpatterns = [
   
    path('', views.schedule, name="class_schedule"),
    path('update/<int:pk>/', views.schedule_update, name="update_schedule")
]