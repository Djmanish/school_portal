# Generated by Django 2.2.7 on 2019-12-24 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class_schedule', '0006_auto_20191221_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='class_stage',
            field=models.CharField(choices=[('Primary', 'Primary'), ('Middle', 'Middle'), ('Highschool', 'Highschool')], max_length=50, null=True),
        ),
    ]