# Generated by Django 2.2.5 on 2019-12-28 05:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Attendance', '0002_auto_20191220_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='daily_status',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='last_name',
        ),
        migrations.AddField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_attendance', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendance',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
