# Generated by Django 2.2.5 on 2020-08-29 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_auto_20200810_2216'),
        ('library', '0002_auto_20200829_1443'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='book',
            unique_together={('book_code', 'book_id', 'book_institute', 'status')},
        ),
    ]