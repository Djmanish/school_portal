
from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView
from .views import RegistrationViewUniqueEmail



urlpatterns = [
  path('', RedirectView.as_view(url='user/login')),
  path('user/register', RegistrationViewUniqueEmail.as_view(), name="register"),
  path('user/dashboard', views.dashboard, name="user_dashboard"),
  path('user/login/', views.login, name="login_user"),
  path('user/profile/', views.user_profile, name="user_profile"),
  path('user/profile/edit/<int:pk>', views.edit_profile, name= 'edit_profile'),
  path('fetch_levels/', views.fetch_levels),
  path('user/approvals',views.approvals, name="approvals"), 

]
