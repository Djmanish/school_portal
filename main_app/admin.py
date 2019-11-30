from django.contrib import admin
from .models import *
from main_app.models import Approvals

# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Institute)  
admin.site.register(Approvals)