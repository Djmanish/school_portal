"""school_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
