# Generated by Django 2.2.7 on 2019-12-18 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holidaylist', '0009_auto_20191218_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holidaylist',
            name='days',
            field=models.CharField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], max_length=10, null=True),
        ),
    ]
