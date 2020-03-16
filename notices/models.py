from django.db import models
from main_app.models import *
from django.contrib.auth.models import User
# Create your models here.


class Notice(models.Model):
    reference_no = models.CharField(max_length=15, null=True, blank=True)
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE, related_name='institute_notices', null=True)
    subject = models.CharField(max_length=150)
    content = models.TextField()
    publish_date = models.DateTimeField()
    category = models.CharField(max_length=15, null=True, blank=True, choices=[('absent','absent')])
    recipients_list = models.ManyToManyField(to=UserProfile )
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, related_name='user_notices')

    def __str__(self):
        return self.subject
