# Generated by Django 2.2.5 on 2020-08-29 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20200829_1509'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookcode',
            unique_together=set(),
        ),
    ]