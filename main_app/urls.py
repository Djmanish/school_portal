
from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView
from .views import RegistrationViewUniqueEmail, InstituteUpdateview



urlpatterns = [
  path('', RedirectView.as_view(url='user/login')),
  path('user/register/', RegistrationViewUniqueEmail.as_view(), name="register"),
  path('user/dashboard/', views.dashboard, name="user_dashboard"),
  path('user/login/', views.login, name="login_user"),
  path('user/profile/', views.user_profile, name="user_profile"),
  path('user/profile/edit/<int:pk>', views.edit_profile, name= 'edit_profile'),
  path('fetch_levels/', views.fetch_levels),
  path('user/approvals/',views.approvals, name="approvals"), 
  path('institute/profile/<int:pk>', views.institute_profile, name='institute_detail'),
  path('institute/profile/edit/<int:pk>',InstituteUpdateview.as_view() , name='edit_institute'),
  path('user/approve/<int:pk>', views.approve_request, name="user_approval"),
  path('user/disapprove/<int:pk>', views.disapprove_request, name="user_disapproval"),
  path('user/classes/',views.classes, name="classes"),
]
