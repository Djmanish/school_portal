# Generated by Django 2.2.7 on 2019-12-28 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('holidaylist', '0013_remove_sendemail_mail_from'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SendEmail',
        ),
    ]
