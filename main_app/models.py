from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.


class Institute(models.Model):
    name = models.CharField(max_length=150)
    profile_pic = models.ImageField(upload_to="Institute Images",default="default_school_pic.jpg" )
    principal = models.CharField(max_length=50)
    about = models.CharField(max_length=300, blank=True, null=True)
    Contact_number = models.CharField(max_length=300)
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
    institute = models.OneToOneField(to=Institute, related_name="institute", on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=25, null=True)
    middle_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length= 25, null = True)
    date_of_birth = models.DateField(null= True)
    about = models.CharField(max_length=300, blank=True, null=True)
    profile_pic = models.ImageField(default="default_profile_pic.jpg", upload_to='UserProfilePictures')
    mobile_number = models.PositiveIntegerField(null=True)
    address_line_1 = models.CharField(max_length= 50 , null= True)
    address_line_2 = models.CharField(max_length=50, null = True)
    city = models.CharField(max_length=50, null=True,)
    state = models.ForeignKey(to=State, on_delete=models.PROTECT, null= True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return str(self.first_name)


