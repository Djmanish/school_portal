from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.fees_home, name="fees_home" ),
    path('parent_fees/', views.parent_fees, name="parent_fees"),
   
    path('create/tag/', views.creating_tags, name="create_fee_tag"),
    path('update/fees/tag/<int:pk>/', Fees_tag_update_view.as_view(), name="fees_tag_update_view" ),
    path('fees_tag/update/history/', views.Fees_Tag_History_List.as_view(), name="fees_tag_history"),
    path('fees/schedule/', views.institute_fees_schedule, name="fees_schedule"),
    path('fees/account/details/', views.institute_account_details, name="fees_account_details"),
    path('mapping/tags/', views.Map_Tag_Students, name="mapping_tags_to_student"),
    path('fetch/class/student/tags/', views.Fetch_student_for_tags, name="student_for_tags"),
    path('fetch/student/tags/', views.fetch_students_tags_mapped, name="fetch_students_tags_mapped"),
    path('students_mapped_to_a_tag/', views.students_mapped_to_a_tag, name="students_mapped_to_a_tag"),
    path('processing/fees/', views.processing_fees, name='processing_fees'),
    path('pay/fees/request/', views.fees_pay_page, name="pay_fees_page"),
    path('handle_requests/', views.handle_requests, name="handle_requests"),
    path('fees/details/', views.view_invoice, name="view_invoice")

]