from django.contrib import admin
from .models import *

# Register your models here.

# Register your models here.
class Student_Tag_Processed_Record_admin(admin.ModelAdmin):
    list_display  = ('institute', 'notification_date', 'process_date','due_date','student',)

class Student_Tags_Record_admin(admin.ModelAdmin):
    list_display= ('institute','student','student_class')

class student_fees_table_admin(admin.ModelAdmin):
    list_display = ('institute','student','due_date','total_due_amount','total_paid','balance')

admin.site.register(School_tags)
admin.site.register(Fees_tag_update_history)
admin.site.register(Fees_Schedule)
admin.site.register(Account_details)
admin.site.register(Student_Tags_Record, Student_Tags_Record_admin)
admin.site.register(Student_Tag_Processed_Record, Student_Tag_Processed_Record_admin)
admin.site.register(Students_fees_table, student_fees_table_admin)
