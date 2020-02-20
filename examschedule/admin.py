
from django.contrib import admin
from .models import *
from examschedule.models import *

# Register your models here.
admin.site.register(ExamType)

admin.site.register(ExamDetails)

