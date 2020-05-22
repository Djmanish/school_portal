from django.contrib import admin
from library.models import *
# Register your models here.
admin.site.register(BookCategory)
admin.site.register(BookSubCategory)
admin.site.register(Book)
admin.site.register(IssueBook)
admin.site.register(BookCode)

