# Generated by Django 2.2.7 on 2020-06-12 09:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examschedule', '0002_auto_20200612_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examdetails',
            name='exam_assign_teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exam_assign_teacher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='examdetails',
            name='exam_subject_teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exam_subject_teacher', to=settings.AUTH_USER_MODEL),
        ),
    ]
