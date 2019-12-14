from django.contrib import admin
from .models import *

# Register your models here.
class Institute_levels_admin(admin.ModelAdmin):
    list_display  = ('institute', 'level_id', 'level_name',)

class Role_Description_admin(admin.ModelAdmin):
    list_display = ('user', 'institute', 'level',)



admin.site.register(UserProfile)
admin.site.register(Institute)
admin.site.register(State)
admin.site.register(Institute_levels, Institute_levels_admin)
admin.site.register(Role_Description, Role_Description_admin)
admin.site.register(Classes)
