# Generated by Django 2.2.7 on 2020-07-15 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20200715_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute',
            name='session_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]