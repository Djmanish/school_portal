# Generated by Django 2.2.7 on 2019-11-22 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20191122_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute',
            name='profile_pic',
            field=models.ImageField(default='default_school_pic.jpg', upload_to='Institute Images'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='full_name',
            field=models.CharField(default='Your Full Name ', max_length=100),
        ),
    ]
