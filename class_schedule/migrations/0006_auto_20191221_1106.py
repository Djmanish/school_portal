# Generated by Django 2.2.7 on 2019-12-21 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class_schedule', '0005_auto_20191220_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]