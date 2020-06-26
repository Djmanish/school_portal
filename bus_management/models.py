from django.db import models
from main_app.models import *
from datetime import date

# Create your models here.
class Bus(models.Model):
    Chi1 =[
        ('active', 'Active'),('inactive', 'Inactive'),    
    ]
    bus_no = models.CharField(max_length=10)
    bus_maker = models.CharField(max_length=15, null=True)
    vehicle_type = models.CharField(max_length=15, null=True)
    fuel_type = models.CharField(max_length=15, null=True)
    bus_color = models.CharField(max_length=10, null=True)
    bus_capacity = models.IntegerField(null=True)
    bus_institute = models.ForeignKey(to=Institute, related_name="bus_institute", on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=25,choices=Chi1,default="active")
    def __str__(self):
       return self.bus_no

class Point(models.Model):
    point_code = models.CharField(max_length=10)
    point_name = models.CharField(max_length=10)
    point_street_no = models.IntegerField(null=True, blank=True)
    point_landmark = models.CharField(max_length=15)
    point_city = models.CharField(max_length=20)
    point_state = models.ForeignKey(to=State, on_delete=models.PROTECT, null= True, blank=True)
    point_country = models.CharField(max_length=20)
    point_institute = models.ForeignKey(to=Institute, related_name="point_institute", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.point_name
