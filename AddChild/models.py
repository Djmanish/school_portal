from django.db import models
from main_app.models import *
from datetime import date
# Create your models here.
class AddChild(models.Model):
   STATUS_CHOICES = (
      ("pending", "pending"),
      ("active", "active"),)
   parent = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE,null=True, related_name="parent" )
   child = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE,null=True, related_name="child")
   institute = models.ForeignKey(to=Institute, related_name="studnt_institute", on_delete=models.PROTECT, null=True, blank=True, default="")
   Class = models.ForeignKey(to=Classes, on_delete=models.PROTECT,blank=True, null=True, related_name='stu_class')
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   status = models.CharField(max_length=9,choices=STATUS_CHOICES,default="pending")
   def approve(self):
        self.status= 'active'
        self.save()
    
   def disapprove(self):
        self.status= 'pending'
        self.save()

   def __str__(self):
      return str(self.parent)