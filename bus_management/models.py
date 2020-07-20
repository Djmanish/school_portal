from django.db import models
from main_app.models import *
from datetime import date
from django.utils import timezone

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
    Chi =[
        ('active', 'Active'),('inactive', 'Inactive'),    
    ]
    point_code = models.CharField(max_length=10)
    point_name = models.CharField(max_length=30)
    point_street_no = models.IntegerField(null=True, blank=True)
    point_landmark = models.CharField(max_length=15)
    point_exact_place = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    point_city = models.CharField(max_length=20)
    point_state = models.ForeignKey(to=State, on_delete=models.PROTECT, null= True, blank=True)
    point_country = models.CharField(max_length=20)
    status = models.CharField(max_length=25,choices=Chi,default="active")
    point_institute = models.ForeignKey(to=Institute, related_name="point_institute", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.point_name

class Driver(models.Model):
    driver_id = models.CharField(max_length=10)
    name = models.OneToOneField(to=UserProfile, on_delete=models.CASCADE, related_name='driver', default=None)
    driving_lic_no = models.CharField(max_length=13)
    institute = models.ForeignKey(to=Institute, related_name="driver_institute", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return str(self.name)

class RouteInfo(models.Model):
    route_no = models.CharField(max_length=20, null=True)
    route_name = models.CharField(max_length=100, null=True)
    vehicle = models.ForeignKey(to=Bus, on_delete=models.CASCADE, related_name='vehicle', null=True, blank=False)
    vehicle_driver = models.ForeignKey(to=Driver, on_delete=models.CASCADE, related_name='driver', null=True, blank=False)
    institute = models.ForeignKey(to=Institute, related_name="route_institute", on_delete=models.CASCADE, null=True, blank=True)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    def __str__(self):
        return self.route_name

class RouteMap(models.Model):
    route = models.ForeignKey(to=RouteInfo, on_delete=models.CASCADE, related_name='route', null=True, blank=False)
    point = models.ForeignKey(to=Point, on_delete=models.CASCADE, related_name='point', null=True, blank=False)
    routemap_institute = models.ForeignKey(to=Institute, related_name="routemap_institute", on_delete=models.CASCADE, null=True, blank=True)
    index = models.IntegerField(default=0)
    time = models.TimeField()

    def __str__(self):
        return str(self.route)
        
class InstituteLocation(models.Model):
    institute = models.OneToOneField(to=Institute, on_delete=models.CASCADE, related_name='transport_institute', default=None)
    longitute = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    def __str__(self):
        return str(self.institute)

class BusUsers(models.Model):
    user = models.OneToOneField(to=UserProfile, on_delete=models.CASCADE, related_name='bus_users')
    point = models.ForeignKey(to=Point, on_delete=models.CASCADE)
    institute = models.ForeignKey(to=Institute, related_name="user_institute", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return str(self.user)

class Trip(models.Model):
    route = models.ForeignKey(to=RouteInfo, on_delete=models.CASCADE, related_name='trip_route', null=True, blank=False)
    point = models.ForeignKey(to=Point, on_delete=models.CASCADE, null=True)
    driver = models.ForeignKey(to=Driver, on_delete=models.CASCADE, related_name='trip_driver', null=True, blank=False)
    time = models.TimeField()
    date = models.DateField()
    def __str__(self):
        return str(self.route)