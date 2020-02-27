from django.urls import path
from . import views


urlpatterns = [
    path('', views.admission_home, name="admission_home" ),
    path('fetch_intitute_classes_for_admission/',views.fetch_institute_class_admission),
]