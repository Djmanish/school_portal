# Generated by Django 2.1.7 on 2020-05-05 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_merge_20200505_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default_school_pic.jpg', null=True, upload_to='Institute Images'),
        ),
    ]
