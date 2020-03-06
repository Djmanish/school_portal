from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_notices, name="all_notice_list"),
    path('create/', views.create_notice, name="create_notice"),
    path('notice/new/' , views.creating_new_notice, name="creating_new_notice")
]