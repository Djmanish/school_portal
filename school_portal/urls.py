
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 
from main_app import views as main_app_views
from rest_framework.urlpatterns import format_suffix_patterns
from main_app.views import userList, userLoginData
from rest_framework.authtoken import views as authviews
from rest_framework_jwt.views import obtain_jwt_token
from notices import views as notice_views
from API_Data.router import router
from API_Data.views import *


urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('bus/', include('bus_management.urls')),
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
    path('api/', include('API_Data.urls')),
    

   

    

   # API URL
    path('users/', userList.as_view()),
    path('users_login_data/', userLoginData.as_view()),
    path('api-token-auth/', obtain_jwt_token),
    path('api/',include(router.urls)),
    path('accounts/activate/', VerifyEmail.as_view(), name="email-verify"),
    path('accounts/password/reset/confirm/<uidb64>/set-password/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
   

    path('notice/view/time/', notice_views.last_notice_view_time)
    
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
