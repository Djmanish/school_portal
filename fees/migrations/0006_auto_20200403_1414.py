# Generated by Django 2.1.7 on 2020-04-03 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0005_fees_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fees_schedule',
            name='institute',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='institute_schedule', to='main_app.Institute'),
        ),
    ]