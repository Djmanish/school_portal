from django.urls import path
from . import views
from .views import Edit_Notice_view

urlpatterns = [
    path('', views.all_notices, name="all_notice_list"),
    path('create/', views.create_notice, name="create_notice"),
    path('notice/new/' , views.creating_new_notice, name="creating_new_notice"),
    path('update/<int:pk>/', Edit_Notice_view.as_view(), name="notice_update"),
    path('fetch_deleted_id/<int:pk>/', views.fetch_deleted_id, name="fetch_delete_id"),
    path('delete_notice/', views.delete_notice, name="delete_notice")


    
]