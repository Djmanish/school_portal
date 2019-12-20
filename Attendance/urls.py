from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView




urlpatterns = [
    path('attendance/',views.attendance ,name='attendance'),
  


]
