from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView




urlpatterns = [
    path('',views.library,name='library'),
    path('book/',views.book,name='book'),
    path('add_category/',views.add_category,name='add_category'),
    path('add_sub_category/',views.add_sub_category,name='add_sub_category'),
    path('add_book/',views.add_book,name='add_book'),
    path('add_book_group/',views.add_book_group,name='add_book_group'),
    path('add_new_book/',views.add_new_book,name='add_new_book'),
    path('issuebook/',views.issuebook,name='issuebook'),
    path('fetch_user_data/',views.fetch_user_data,name='fetch_user_data'),
    path('issue_book/',views.issue_book,name='issue_book'),
    path('book_return/',views.book_return,name='book_return'),
    path('return_book/',views.return_book,name='return_book'),
]
