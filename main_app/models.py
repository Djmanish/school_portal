from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Institute(models.Model):
     Name: models.CharField(max_length=255)
     # attributes here




class Userprofile(models.Model):
     user = models.OneToOneField(to=User, on_delete=models.CASCADE)
     full_name = models.CharField(max_length=100)
     # attributes here





class Instituteprofile(models.Model):
     institute = models.OneToOneField(to=Institute, on_delete= models.CASCADE)
     # attributes here

