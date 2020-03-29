from django.urls import path
from . import views

urlpatterns = [
    path('', views.fees_home, name="fees_home" )
]