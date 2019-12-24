
from django.urls import path, include
from . import views
from .views import  Update_lecture_time




urlpatterns = [
   
    path('', views.schedule, name="class_schedule"),
    path('update/<int:pk>/', views.schedule_update, name="update_schedule"),
    path('update/lectures/',views.class_stage_lecture_time_update, name="lectures_list"),
    path('update/timing/<int:pk>', Update_lecture_time.as_view(), name="lecture_time"),
    path('class_stage/_all_lectures/<int:id>/', views.class_stage_all_lectures, name="class_stage_lectures")
]