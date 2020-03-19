
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 
from main_app import views as main_app_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
   
    path('addchild/', include('AddChild.urls')),
    path('attendance/', include('Attendance.urls')),
    path('accounts/', include('registration.backends.default.urls')),
    path('schedule/', include('class_schedule.urls')),
    path('holiday/', include('holidaylist.urls')),
    path('examschedule/', include('examschedule.urls')),
    path('examresult/',include('exam_result.urls')),
    path('not_found/', main_app_views.not_found_page, name="not_found" ),
    path('admission_process/', include('admissions.urls')),
    path('notice/', include('notices.urls') )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
