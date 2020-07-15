from django.urls import path, include
from django.http import HttpResponse

from . import views
from .views import *

# from holidaylist.views import add_holiday




urlpatterns = [
  
  path('examresult/<int:pk>', views.exam_result, name="examresult"),
  path('exam_result/<int:pk>',views.examresult, name="exam_result"),
  path('studentview/<int:pk>', views.student_view, name="studentview"),
  path('fetching_sr_no/', views.fetch_sr_no, name='fetch_result_sr_no' ),
  path('report_card/<int:pk>',views.report_card, name='report_card'),
  path('reports_card/<int:pk>',views.reports_card, name='reports_card'),
  path('selected_exam_types/', views.selected_exam_type, name='selected_exam_type' ),

  path('chart_sr_no/', views.chart_sr_no, name='chart_sr_no'),
  path('overall_result/<int:pk>/<int:student_pk>/', views.overall_result, name='overall_result'),
  path('overall_report_card/<int:pk>/<int:student_pk>/', views.overall_report_card, name='overall_report_card'),

  path('class_promotion/<int:pk>/', views.class_promotion, name="class_promotion"),
  
  path('result/', views.st_result, name="st_result")
 
              ]
