
from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView
from .views import RegistrationViewUniqueEmail
from .views import Profile_update_View

urlpatterns = [
  path('', RedirectView.as_view(url='user/login')),
  path('user/register', RegistrationViewUniqueEmail.as_view(), name="register"),
  path('user/dashboard', views.dashboard, name="user_dashboard"),
  path('user/login/', views.login, name="login_user"),
  path('user/profile/', views.user_profile, name="user_profile"),
  path('user/profile/edit/<int:pk>/', Profile_update_View.as_view(), name='edit_profile' ),

]
