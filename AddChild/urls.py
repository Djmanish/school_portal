from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView




urlpatterns = [
    path('',views.addchild,name='addchild'),
    path('fetch_intitute_classes/', views.fetch_institute_class, name="fectch_institute_classes"),
    path('addchildtolist/<int:pk>/',views.addchildtolist, name="addchildtolist"),
    path('approve/<int:pk>/', views.approve_child_request, name="child_approval"),
    path('disapprove/<int:pk>/', views.disapprove_child_request, name="child_disapproval"),
    path('childview/<int:pk>/',views.childview,name="childview"),
    
    
    

  


]
