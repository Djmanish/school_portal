from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView
from django.conf.urls import url




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
    path('fetch_sub_category/', views.fetch_sub_category, name="fetch_sub_category"),
    path('lib_settings/',views.lib_settings,name='lib_settings'),
    path('edit_book/',views.edit_book,name='edit_book'),
    path('delete_book/<int:pk>/',views.delete_book,name='delete_book'),
    path('add_more_books/',views.add_more_books,name='add_more_books'),
    path('add_new_books/',views.add_new_books,name='add_new_books'),
    path('see_all/',views.see_all,name='see_all'),
    path('show_qr/',views.show_qr,name='show_qr'),
    path('view_book/<int:pk>/',views.view_book,name='view_book'),
    path('delete_view_book/<int:pk>/',views.delete_view_book,name='delete_view_book'),
    path('fetch_book_ids/',views.fetch_book_ids,name='fetch_book_ids'),
    path('api/users', views.UserCreate.as_view(), name='account-create'),
    
    
]
