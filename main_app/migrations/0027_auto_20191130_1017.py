# Generated by Django 2.2.7 on 2019-11-30 04:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0026_user_extention'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role_description',
            name='user_role',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_institute_role', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User_extention',
        ),
    ]
