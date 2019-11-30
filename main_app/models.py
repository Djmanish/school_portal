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





class UserProfile(models.Model):
    User_choices=[('Pending','Pending'),('Approve','Approve'),('Disapprove','Disapprove')]
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    institute = models.OneToOneField(to=Institute, related_name="institute", on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, default="Your Full Name ")
    about = models.CharField(max_length=300, blank=True, null=True)
    profile_pic = models.ImageField(default="default_profile_pic.jpg", upload_to='UserProfilePictures')
    mobile_number = models.PositiveIntegerField(null=True)
    address = models.TextField(null=True)
    city = models.CharField(max_length=50, null=True,)
    state = models.CharField(max_length=50, null=True)
    facebook_link = models.URLField(null=True, blank=True)
    Status =models.CharField(max_length=50,choices=User_choices,default="Pending")
    def __str__(self):
        return self.full_name


class Approvals(models.Model):
    User_choices=[('Pending','Pending'),('Approve','Approve'),('Disapprove','Disapprove')]
    Username = models.OneToOneField(to=UserProfile,on_delete=models.CASCADE, related_name='profile')
    Assignee = models.CharField(max_length=50,default="SiteAdmin")
    Request_date = models.DateTimeField(auto_now_add= True)
    Action_date =models.DateTimeField(auto_now=True)
    Status =models.CharField(max_length=50,choices=User_choices,default="Pending")

    def __str__(self):
        return self.full_name


