from django.contrib import admin
from .models import *

from exam_result.models import *

# Register your models here.
admin.site.register(ExamResult)
admin.site.register(CalculateResult)
# admin.site.register(Overall)

