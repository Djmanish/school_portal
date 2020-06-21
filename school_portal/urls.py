
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 
from main_app import views as main_app_views
from rest_framework.urlpatterns import format_suffix_patterns
from main_app.views import userList, userLoginData
from rest_framework.authtoken import views as authviews
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('library/', include('library.urls')),
    path('addchild/', include('AddChild.urls')),
    path('attendance/', include('Attendance.urls')),
    path('accounts/', include('registration.backends.default.urls')),
    path('schedule/', include('class_schedule.urls')),
    path('holiday/', include('holidaylist.urls')),
    path('examschedule/', include('examschedule.urls')),
    path('examresult/',include('exam_result.urls')),
    path('not_found/', main_app_views.not_found_page, name="not_found" ),
    path('admission_process/', include('admissions.urls')),
    path('notice/', include('notices.urls') ),
    path('fees/', include('fees.urls')),
   # API URL
    path('users/', userList.as_view()),
    path('users_login_data/', userLoginData.as_view()),
    path('api-token-auth/', obtain_jwt_token),
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
