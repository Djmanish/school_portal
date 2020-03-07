from django.db import models
from main_app.models import *

# Create your models here.


class Notice(models.Model):
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE, related_name='institute_notices', null=True)
    subject = models.CharField(max_length=150)
    content = models.TextField()
    publish_date = models.DateTimeField()
    recipients_list = models.ManyToManyField(to=UserProfile )

    def __str__(self):
        return self.subject
