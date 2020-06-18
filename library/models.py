from django.db import models
from main_app.models import *
from datetime import date
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw 

# Create your models here.
class BookCategory(models.Model):
    book_category_name = models.CharField(max_length=50)
    institute_category = models.ForeignKey(to=Institute, related_name="category_institute", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
       return self.book_category_name

class BookSubCategory(models.Model):
    book_sub_category_name = models.CharField(max_length=50)
    parent_category=models.ForeignKey(to=BookCategory, on_delete=models.PROTECT, related_name='book_sub_category', null=True, blank=True)
    institute_subcategory= models.ForeignKey(to=Institute, related_name="institute_subcategory", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
       return self.book_sub_category_name

class BookCode(models.Model):
    Chi1 =[
        ('active', 'Active'),('inactive', 'Inactive'),
        
    ]
    code=models.CharField(max_length=20, null=True)
    book_count= models.IntegerField(null=True)
    book_institute = models.ForeignKey(to=Institute, related_name="bookcode_institute", on_delete=models.CASCADE, null=True, blank=True)
    book_name= models.CharField(max_length=50)
    book_category= models.ForeignKey(to=BookCategory,on_delete=models.PROTECT, related_name='bookcode_category')
    book_sub_category= models.ForeignKey(to=BookSubCategory,on_delete=models.PROTECT, related_name='bookcode_sub_category')
    author= models.CharField(max_length=50)
    publications= models.CharField(max_length=50)
    edition= models.CharField(max_length=50)
    status = models.CharField(max_length=25,choices=Chi1,default="active")
    class Meta:
        unique_together = ['code', 'book_institute']
    def __str__(self):
        return self.code

class Book(models.Model):
    Chi2 =[
        ('active', 'Active'),('inactive', 'Inactive'),
        
    ]
    book_code=models.CharField(max_length=20, null=True)
    book_id= models.CharField(max_length=20, null=True)
    book_institute = models.ForeignKey(to=Institute, related_name="book_institute", on_delete=models.CASCADE, null=True, blank=True)
    book_name= models.CharField(max_length=50)
    book_category= models.ForeignKey(to=BookCategory,on_delete=models.PROTECT, related_name='book_category')
    book_sub_category= models.ForeignKey(to=BookSubCategory,on_delete=models.PROTECT, related_name='book_sub_category')
    author= models.CharField(max_length=50)
    publications= models.CharField(max_length=50)
    edition= models.CharField(max_length=50)
    book_count= models.IntegerField(null=True)
    status = models.CharField(max_length=25,choices=Chi2,default="active")
    qr_codes = models.ImageField(upload_to='QrCodes', blank=True)
    class Meta:
        unique_together = ['book_code', 'book_id', 'book_institute']
    def __str__(self):
       return self.book_name

    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=0,
        )
        qr.add_data(self.book_id)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        # qrcode_img = qrcode.make(self.book_id)
        canvas = Image.new('RGB', (213, 205), 'white')
        draw =ImageDraw.Draw(canvas)
        canvas.paste(img)
        fname = f'{self.book_id}-{self.book_name}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_codes.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

class IssueBook(models.Model):
    user_name= models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='user_name', null=True, blank=False)
    book_name= models.ForeignKey(to=Book, on_delete=models.PROTECT, related_name='issued_book_name', null=True, blank=False)
    issue_book_institute = models.ForeignKey(to=Institute, related_name="issue_book_institute", on_delete=models.CASCADE, null=True, blank=True)
    issued_by= models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='issued_by', null=True, blank=False)
    issued_date= models.DateTimeField(null=True,)
    expiry_date= models.DateTimeField(null=True)
    return_date= models.DateTimeField(null=True, blank=True)
    description= models.TextField(blank=True)
    delay_counter= models.IntegerField(null=True, blank=True)
    late_fine = models.IntegerField(null=True, blank=True)
    damage_fine= models.IntegerField(default=0)
    updated_by= models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='updated_by', null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
       return str(self.user_name)

class LibrarySettings(models.Model):
    institute= models.OneToOneField(to=Institute, related_name="library_settings", on_delete=models.CASCADE, null=True, blank=True)
    max_Book_Allows= models.IntegerField(null=True, blank=True)
    day_Span= models.IntegerField(null=True, blank=True)
    send_Reminder_Before= models.IntegerField(null=True, blank=True)
    late_fine_per_day = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return str(self.institute)

# class IssueDays(models.Model):
#     institute= models.ForeignKey(to=Institute, related_name="institute_issue_days", on_delete=models.CASCADE, null=True, blank=True)
#     issue_days= models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return self.issue_days