from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from .models import *
from main_app.models import *
from notices.models import *
from django.utils import timezone



# starting signal for creating parents child notification category when institute is created
@receiver(post_save, sender=Institute)
def parents_child_notice_category(sender, instance, created, **kwargs):
    if created:
        try:
            Notification_Category.objects.get(name="Parents Child", institute= instance)
        except:
            Notification_Category.objects.create(name="Parents Child", institute= instance)
# ending signal for creating parents child notification category when institute is created



@receiver(post_save, sender=AddChild)
def child_approved(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        if instance.status =='active':
            try:
                parent_child_category = Notification_Category.objects.get(institute=instance.institute, name="Parents Child")
            except:
                create_category = Notification_Category.objects.create(name="Parents Child", institute= instance.institute)
                parent_child_category = create_category
            
            parent_child_notice = Notice.objects.create(institute = instance.institute, category=parent_child_category, subject =f"Your request for child approved", content=f"Your request to add {instance.child.first_name} {instance.child.last_name} as child approved.", created_at= timezone.now(), publish_date= timezone.now() )

            parent = AddChild.objects.get(pk= instance.id)
            parent_child_notice.recipients_list.add(parent.parent)
