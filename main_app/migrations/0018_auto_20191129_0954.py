# Generated by Django 2.2.7 on 2019-11-29 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_auto_20191129_0949'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='institute_levels',
            unique_together={('institute', 'level_name')},
        ),
    ]