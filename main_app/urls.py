
from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView
from .views import RegistrationViewUniqueEmail

urlpatterns = [
  path('', RedirectView.as_view(url='user/login')),
  path('user/register', RegistrationViewUniqueEmail.as_view(), name="register"),

  path('user/dashboard', views.dashboard, name="user_dashboard"),
  path('user/login/', views.login, name="login_user"),

]
