# Generated by Django 2.2.5 on 2020-08-29 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20200829_1501'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='book',
            unique_together=set(),
        ),
    ]