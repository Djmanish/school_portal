# Generated by Django 2.2.5 on 2020-06-11 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20200610_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='qr_codes',
            field=models.ImageField(blank=True, upload_to='QrCodes'),
        ),
    ]
