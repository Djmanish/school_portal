# Generated by Django 2.2.7 on 2019-12-02 03:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0027_auto_20191130_1017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role_description',
            name='user_role',
        ),
        migrations.AddField(
            model_name='role_description',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_institute_role', to=settings.AUTH_USER_MODEL),
        ),
    ]
