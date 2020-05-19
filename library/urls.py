from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView




urlpatterns = [
    path('',views.library,name='library'),
    path('book/',views.book,name='book'),
    path('add_category/',views.add_category,name='add_category')
]
