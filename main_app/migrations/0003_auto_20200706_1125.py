# Generated by Django 3.0.8 on 2020-07-06 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20200703_1524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student_info',
            old_name='blood_group',
            new_name='student_blood_group',
        ),
    ]
