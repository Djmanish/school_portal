from django.contrib import admin
from .models import *
from holidaylist.models import *

# Register your models here.
admin.site.register(HolidayList)
# admin.site.register(SendEmail)