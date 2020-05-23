from django.db import models
from main_app.models import *
from datetime import date

# Create your models here.
class BookCategory(models.Model):
    book_category_name = models.CharField(max_length=50)
    institute_category = models.ForeignKey(to=Institute, related_name="category_institute", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
       return self.book_category_name

class BookSubCategory(models.Model):
    book_sub_category_name = models.CharField(max_length=50)
    parent_category=models.ForeignKey(to=BookCategory, on_delete=models.CASCADE, related_name='book_sub_category', null=True, blank=True)
    institute_subcategory= models.ForeignKey(to=Institute, related_name="institute_subcategory", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
       return self.book_sub_category_name

class Book(models.Model):
    book_code=models.CharField(max_length=20, null=True)
    book_id= models.CharField(max_length=20, null=True)
    book_institute = models.ForeignKey(to=Institute, related_name="book_institute", on_delete=models.PROTECT, null=True, blank=True)
    book_name= models.CharField(max_length=50)
    book_category= models.ForeignKey(to=BookCategory,on_delete=models.CASCADE, related_name='book_category')
    book_sub_category= models.ForeignKey(to=BookSubCategory,on_delete=models.CASCADE, related_name='book_sub_category')
    author= models.CharField(max_length=50)
    publications= models.CharField(max_length=50)
    edition= models.CharField(max_length=50)
    book_count= models.IntegerField(null=True)
    def __str__(self):
       return self.book_name

class IssueBook(models.Model):
    user_name= models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='user_name', null=False, blank=False)
    book_name= models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name='issued_book_name', null=False, blank=False)
    issue_book_institute = models.ForeignKey(to=Institute, related_name="issue_book_institute", on_delete=models.CASCADE, null=True, blank=True)
    issued_by= models.CharField(max_length=50)
    issued_date= models.DateTimeField(null=True)
    expiry_date= models.DateTimeField(null=True)
    return_date= models.DateTimeField(null=True, blank=True)
    description= models.TextField(max_length=100, blank=True)
    delay_counter= models.IntegerField(null=True, blank= True)

    def __str__(self):
       return str(self.user_name)

