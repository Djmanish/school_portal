from django.db import models
from main_app.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.

class School_tags(models.Model):
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE, related_name='institute_fees_tags', null=True)
    fees_code = models.CharField(max_length=15, null=True)
    description = models.TextField(null=True)
    type= models.CharField(max_length=7, choices = [('debit','debit'),('credit','credit')], null=True)
    active = models.CharField(max_length=5, choices = [('yes','yes'),('no','no')], null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    tax_percentage = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    amount_including_tax = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def validate_unique(self,exclude=None):
        try:
            super(School_tags,self).validate_unique()
        except ValidationError as e:
            raise ValidationError(self.fees_code+" Tag with this fees code already exists !!! ") 
    class Meta:
        unique_together = ('institute','fees_code')

    def __str__(self):
        return self.description


class Fees_tag_update_history(models.Model):
    fees_tag = models.ForeignKey(to=School_tags, on_delete=models.CASCADE, null=True, related_name='tags_updates')
    date = models.DateTimeField()
    update_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="fees_tag_updates")
    old_values = models.TextField(null=True)
    new_values = models.TextField(null=True)
    
    def __str__(self):
        return str(self.fees_tag)

class Fees_Schedule(models.Model):
    institute = models.OneToOneField(to=Institute, on_delete=models.CASCADE, related_name="institute_schedule")
    notification_date = models.DateField()
    due_date = models.DateField()
    processing_date = models.DateField()

    def __str__(self):
        return str(self.institute)

class Account_details(models.Model):
    institute = models.OneToOneField(to=Institute, on_delete=models.CASCADE, related_name="institute_account_details")
    merchant_id = models.CharField(max_length=25)
    merchant_key = models.CharField(max_length=25)
    def __str__(self):
        return str(self.institute)
   

class Student_Tags_Record(models.Model):
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE, null=True)
    student = models.OneToOneField(to=UserProfile, on_delete=models.CASCADE, related_name="student_tags")
    tags = models.ManyToManyField(to=School_tags, related_name="tags_to_student")
    student_class = models.ForeignKey(to=Classes, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.student)

class Student_Tag_Processed_Record(models.Model):
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE, null=True)
    notification_date = models.DateField(null=True) # notification date
    process_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    student = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, null=True )
    fees_code = models.CharField(max_length=15, null=True)
    description = models.TextField(null=True)
    type= models.CharField(max_length=7, null=True)
    active = models.CharField(max_length=5, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    tax_percentage = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    amount_including_tax = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    class Meta:
        unique_together = ('institute','process_date','student','fees_code')
    def __str__(self):
        return str(self.student.first_name) +" "+ str(self.student.last_name) 

# students fees summary table
class Students_fees_table(models.Model):
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='studnts_fees_info', null=True)
    due_date = models.DateField(null=True)
    invoice_number = models.CharField(max_length=20, null=True)
    total_due_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    
    def __str__(self):
        return str(self.student)