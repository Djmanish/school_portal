from django.urls import path
from . import views
from .views import Admission_Requests_View, Admission_Request_Detail_View


urlpatterns = [
    path('', views.admission_home, name="admission_home" ),
    path('fetch_intitute_classes_for_admission/',views.fetch_institute_class_admission),
    path('admission_requests/', Admission_Requests_View.as_view(), name="admission_requests"),
    path('admission_request_detail/<int:pk>', Admission_Request_Detail_View.as_view(), name="admission_request")
]