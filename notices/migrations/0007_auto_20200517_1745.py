# Generated by Django 2.1.7 on 2020-05-17 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0006_auto_20200517_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
