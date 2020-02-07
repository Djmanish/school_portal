from django.contrib import admin

from Attendance.models import Attendance
#  Register your models here.

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('__str__','institute','student_class','attendance_status','date',)
    
    search_fields = ('student__username',)
    



admin.site.register(Attendance, AttendanceAdmin)
