# Generated by Django 2.2.7 on 2020-03-07 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0002_notice_institute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='subject',
            field=models.CharField(max_length=150),
        ),
    ]
