# Generated by Django 2.2.7 on 2020-08-10 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20200810_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='name',
            field=models.CharField(default='Select State', max_length=35),
        ),
    ]
