from django.db import models
from django.core.validators import validate_email, RegexValidator
from main_app.models import *

# Create your models here.

class Admission_Query(models.Model):
    
    first_name = models.CharField(max_length=20, verbose_name="First Name",)
    middle_name =  models.CharField(max_length=20, blank= True, null= True, )
    last_name =  models.CharField(max_length=20, blank= True, null= True, )
    father_name = models.CharField(max_length=30, null=True)
    mother_name = models.CharField(max_length=30, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(choices = [('Male','Male'), ('Female','Female'),('Other','Other')], max_length=9, null=True)
    Category = models.CharField(choices = [('General','General'),('sc/st','SC/ST'), ('OBC','OBC') ],  max_length=10, null=True)
    school_name = models.ForeignKey(to=Institute, null=True, on_delete= models.SET_NULL, related_name='admission_request')
    class_name = models.ForeignKey(to=Classes, null=True, on_delete=models.SET_NULL, related_name='requested_school_class')
    mobile_Number =models.CharField( max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], null=True)
    Email_Id = models.CharField(validators=[validate_email], max_length=100,blank= True, null= True,)
    Nationality = models.CharField(choices = [('Indian','Indian'), ('Other','Other')],  max_length=10, null=True)
    Address = models.CharField(max_length=100, null=True)
    District = models.CharField(max_length=20, null=True)
    State = models.ForeignKey(to= State, on_delete = models.SET_NULL, null=True )
    Pin_Code = models.IntegerField(null=True)
    Student_Photo = models.ImageField( upload_to='Student_Photos', null=True)
    
   
    def __str__(self):
        return f"{self.first_name} "
