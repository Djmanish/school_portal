from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from notices.models import Notification_Category


# starting signal for creating Holiday notification category when institute is created
@receiver(post_save, sender=Institute)
def HolidayNoticeCategory(sender, instance, created, **kwargs):
    if created:
        try:
            Notification_Category.objects.get(name="Holiday", institute= instance)
        except:
            Notification_Category.objects.create(name="Holiday", institute= instance)
# ending signal for creating Holiday notification category when institute is created