# Generated by Django 2.2.5 on 2020-01-06 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
        ('Attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='Class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='attendance_class', to='main_app.Classes'),
        ),
    ]