# Generated by Django 2.2.7 on 2020-01-25 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examschedule', '0019_auto_20200125_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examschedule',
            name='test_time1',
            field=models.DateTimeField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='examschedule',
            name='test_time2',
            field=models.DateTimeField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='examschedule',
            name='test_time3',
            field=models.DateTimeField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='examschedule',
            name='test_time4',
            field=models.DateTimeField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='examschedule',
            name='test_time5',
            field=models.DateTimeField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='examschedule',
            name='test_time6',
            field=models.DateTimeField(max_length=100, null=True),
        ),
    ]
