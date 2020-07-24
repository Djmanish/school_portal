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
   
    