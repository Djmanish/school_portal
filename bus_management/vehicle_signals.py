from django.dispatch.dispatcher import Signal, receiver
from django.db.models.signals import post_save
from django.utils import timezone
from .models import *
from notices.models import *
from django.contrib.auth.signals import user_logged_in
from AddChild.models import *



# Starting Custom signal for start bus

start = Signal(providing_args=['route','request'])
@receiver(start)
def vehicle_start_notification(sender, **kwargs):
    try:
        r = kwargs['route']        
        ind1 = RouteMap.objects.get(route=r, index=1)
        ind2 = RouteMap.objects.get(route=r, index=2)
        user1 = BusUsers.objects.filter(point=ind1.point)
        user2 = BusUsers.objects.filter(point=ind2.point)
        u = user1 | user2
        print("Hello User")
        a=[]
        for d in u:
            a.append(d.user)
            if d.user.designation.level_name == "student":
                print("Inside")
                parent = AddChild.objects.get(child=d.user)
                print(parent)
                a.append(parent.parent)
        for z in a:
            print(z)
        unq = str(ind1.route.id)+str(r)
        try:
            chk_notice = Notice.objects.get(reference_no=unq, created_at=timezone.now())
        except Notice.DoesNotExist:
            vehicle_notice= Notice.objects.create(reference_no=unq ,institute = ind1.point.point_institute, category ='Vehicle', subject =f"Your vehicle is started", content=f"Your vehicle is started and reaching at {ind1.point.point_name}.", created_at= timezone.now(), publish_date= timezone.now() )
            for i in a:
                vehicle_notice.recipients_list.add(i)
        
        # ind2 = RouteMap.objects.get(route=route, index=2)
    except:
        pass

point_map = Signal(providing_args=['route','point','request'])
@receiver(point_map)
def point_map_notification(sender, **kwargs):
    try:
        r = kwargs['route']
        p = kwargs['point']
        s_route= RouteInfo.objects.get(id=r.id)
        s_point= Point.objects.get(id=p.id)
        p_timing= RouteMap.objects.get(route=s_route,point=s_point,routemap_institute=s_point.point_institute)
        print(p_timing)
        users = BusUsers.objects.filter(point=s_point,institute= s_point.point_institute)
        point_notice= Notice.objects.create(institute = s_point.point_institute, category ='Vehicle', subject =f"Your point {s_point.point_name} is mapped with route {s_route.route_name}.", content=f"Your point {s_point.point_name} is mapped with route:-{s_route.route_name}, Vehicle No.:-{s_route.vehicle.bus_no}, Driver:- {s_route.vehicle_driver.name.first_name} {s_route.vehicle_driver.name.last_name} and Timing:- {p_timing.time}", created_at= timezone.now(), publish_date= timezone.now() )
        for i in users:
                point_notice.recipients_list.add(i.user)
    except:
        pass


point_map_del = Signal(providing_args=['route','point','request'])
@receiver(point_map_del)
def point_map_del_notification(sender, **kwargs):
    try:
        r = kwargs['route']
        p = kwargs['point']
        s_route= RouteInfo.objects.get(id=r.id)
        s_point= Point.objects.get(id=p.id)
        users = BusUsers.objects.filter(point=s_point,institute= s_point.point_institute)
        point_notice= Notice.objects.create(institute = s_point.point_institute, category ='Vehicle', subject =f"Your point:- {s_point.point_name} is removed from route:- {s_route.route_name}.", content=f"Your point:- {s_point.point_name} is removed from route:-{s_route.route_name}", created_at= timezone.now(), publish_date= timezone.now() )
        for i in users:
                point_notice.recipients_list.add(i.user)
    except:
        pass




# starting signal for vehicle
  
@receiver(post_save, sender=Trip)
def vehicle_notification(sender, instance, created, **kwargs):
    if created:
        # p = instance.point
        index_no = RouteMap.objects.get(route= instance.route, point__id=instance.point.id)
        try:
            indi = RouteMap.objects.get(route= instance.route,index =int(index_no.index)+2)
            users = BusUsers.objects.filter(point=indi.point)
            vehicle_notice= Notice.objects.create(institute = instance.point.point_institute, category ='Vehicle', subject =f"Your vehicle is arriving soon", content=f"Your vehicle is reached at {instance.point.point_name}, Be ready at your point to pick the vehicle.", created_at= timezone.now(), publish_date= timezone.now() )
            for i in users:
                vehicle_notice.recipients_list.add(i.user)
        except:
            pass
   
    