# Generated by Django 2.2.7 on 2019-11-27 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20191125_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='institute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institute', to='main_app.Institute'),
        ),
    ]
