from django.db import models
from main_app.models import *
from django.contrib.auth.models import User
# Create your models here.

# class Notification_Category(models.Model):
#     institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE, related_name='inst_notice_category', null=True)
#     name = models.CharField(max_length=30, null=True)

#     def __str__(self):
#         return str(self.institute)+" "+str(self.name)



class Notice(models.Model):
    reference_no = models.CharField(max_length=15, null=True, blank=True)
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE, related_name='institute_notices', null=True)
    category = models.CharField(max_length=30, null=True, blank=True)
    subject = models.CharField(max_length=150, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    recipients_list = models.ManyToManyField(to=UserProfile, related_name="users_notice" )
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, related_name='user_notices', blank=True)
    class Meta:
        unique_together = ['reference_no','institute']

    def __str__(self):
        return self.subject

# model for tracking new notice time
class NoticeViewTime(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="user_last_notice_view", null=True)
    last_seen = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.user) + str(self.last_seen)
