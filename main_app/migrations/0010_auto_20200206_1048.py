# Generated by Django 2.1.7 on 2020-02-06 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_auto_20200206_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute_levels',
            name='institute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='institute_levels', to='main_app.Institute'),
        ),
    ]