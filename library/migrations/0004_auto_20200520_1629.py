# Generated by Django 2.2.5 on 2020-05-20 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_remove_userprofile_country'),
        ('library', '0003_auto_20200520_1622'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookcode',
            unique_together={('code', 'book_institute')},
        ),
    ]
