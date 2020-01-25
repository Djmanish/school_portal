from django.urls import path, include
from main_app import views
from . import views

from django.views.generic.base import RedirectView
from .views import RegistrationViewUniqueEmail, InstituteUpdateview, ClassUpdateView, Edit_Role_Permissions





urlpatterns = [
  path('', RedirectView.as_view(url='user/login')),
  path('user/register/', RegistrationViewUniqueEmail.as_view(), name="register"),
  path('user/dashboard/', views.dashboard, name="user_dashboard"),
  path('user/login/', views.login, name="login_user"),
  path('user/profile/', views.user_profile, name="user_profile"),
  path('user/profile/edit/<int:pk>/', views.edit_profile, name= 'edit_profile'),
  path('fetch_levels/', views.fetch_levels),
  path('user/approvals/<int:pk>/',views.approvals, name="approvals"), 
  path('institute/profile/<int:pk>', views.institute_profile, name='institute_detail'),
  path('institute/profile/edit/<int:pk>',InstituteUpdateview.as_view() , name='edit_institute'),
  path('user/approve/<int:pk>/', views.approve_request, name="user_approval"),
  path('user/disapprove/<int:pk>/', views.disapprove_request, name="user_disapproval"),
  # path('user/classes/',views.classes, name="classes"),
  # path('institute/profile/subjects/',views.subjects, name="subjects"),

  path('institute/profile/<int:pk>/', views.institute_profile, name='institute_detail'),
  path('institute/profile/edit/<int:pk>/',InstituteUpdateview.as_view() , name='edit_institute'),
  path('user/approve/<int:pk>/', views.approve_request, name="user_approval"),
  path('user/disapprove/<int:pk>/', views.disapprove_request, name="user_disapproval"),
  path('add/new_role/<int:pk>/', views.add_new_role, name="add_new_role"),
  path('user_role/delete/<int:pk>/', views.delete_user_role, name="delete_user_role"),
  path('user/class/add_class/',views.add_classes, name="add_classes"),
  path('add/new_subject/', views.add_subjects, name="add_subjects"),
  path('subject/edit/<int:pk>/', views.edit_subject, name='edit_subject'),
  path('subject/delete/<int:pk>/', views.delete_subject, name='delete_subject'),

  path('class/edit/<int:pk>/',views.edit_class, name='edit_class'),
  path('class/delete/<int:pk>/',views.delete_class, name='delete_class'),



  path('student/select_class/', views.selecting_class, name="selecting_class"),
  
 
  path('class/<int:pk>/assign_class_teacher', views.assign_class_teacher, name="assign_class_teacher"),

  path('update_role_permissions/<int:pk>/', views.edit_role_permissions, name="role_permissions")


]
