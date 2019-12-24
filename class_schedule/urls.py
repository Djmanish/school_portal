
from django.urls import path, include
from . import views
from .views import LectureListView, Update_lecture_time




urlpatterns = [
   
    path('', views.schedule, name="class_schedule"),
    path('update/<int:pk>/', views.schedule_update, name="update_schedule"),
    path('update/lectures/', LectureListView.as_view(), name="lectures_list"),
    path('update/timing/<int:pk>', Update_lecture_time.as_view(), name="lecture_time")
]