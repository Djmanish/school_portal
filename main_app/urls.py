
from django.urls import path, include
from . import views
from .views import RegistrationViewUniqueEmail

urlpatterns = [
  path('', views.index, name="home_page" ),
  path('user/register', RegistrationViewUniqueEmail.as_view(), name="register"),
  path('user/dashboard', views.dashboard, name="user_dashboard"),
  path('user/login/', views.login, name="login_user"),

]
