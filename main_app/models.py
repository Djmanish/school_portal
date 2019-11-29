from django.db import models
from django.contrib.auth.models import User, AbstractUser
from datetime import date

# Create your models here.


class Institute(models.Model):
    name = models.CharField(max_length=150)
    profile_pic = models.ImageField(upload_to="Institute Images",default="default_school_pic.jpg" )
    principal = models.CharField(max_length=50, null=True)
    about = models.CharField(max_length=300, blank=True, default="This is about Institute" )
    Contact_number = models.CharField(max_length=12, )
    address = models.TextField( null=True)
    email = models.EmailField(null=True)
    
    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=35)
    def __str__(self):
        return self.name



class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    institute = models.ForeignKey(to=Institute, related_name="institute", on_delete=models.PROTECT, null=True, blank=True, default="")
    designation = models.ForeignKey('Institute_levels', on_delete=models.PROTECT, related_name='user_designation', null=True)
    first_name = models.CharField(max_length=25, null=True, default="")
    middle_name = models.CharField(max_length=20, null=True, default="")
    last_name = models.CharField(max_length= 25, null = True,default="")
    date_of_birth = models.DateField(null= True,  default=date.today)
    about = models.CharField(max_length=300, blank=True, null=True, default="About yourself")
    profile_pic = models.ImageField(default="default_profile_pic.jpg", upload_to='UserProfilePictures')
    mobile_number = models.PositiveIntegerField(null=True, default="999999999")
    address_line_1 = models.CharField(max_length= 50 , null= True, default="Address line 1")
    address_line_2 = models.CharField(max_length=50, null = True, default="Address line 2")
    city = models.CharField(max_length=50, null=True, default="City")
    state = models.ForeignKey(to=State, on_delete=models.PROTECT, null= True, blank=True)
    facebook_link = models.URLField(null=True, blank=True, default="https://www.facebook.com/")
    
    def __str__(self):
        return str(self.first_name)


class Institute_levels(models.Model):
    institute= models.ForeignKey(to=Institute, on_delete=models.CASCADE, related_name='institute_levels')
    level_id= models.CharField(max_length=2, null=True)
    level_name = models.CharField(max_length=25)
    
    def __str__(self):
        return self.level_name
