# Generated by Django 2.2.7 on 2020-03-17 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20200317_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='class_next_year',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='class_promotion_status',
            field=models.CharField(choices=[('Promoted', 'Promoted'), ('Not Promoted', 'Not Promoted')], default='Promoted', max_length=30, null=True),
        ),
    ]
