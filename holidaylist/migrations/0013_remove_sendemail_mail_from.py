# Generated by Django 2.2.7 on 2019-12-28 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('holidaylist', '0012_sendemail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sendemail',
            name='mail_from',
        ),
    ]
