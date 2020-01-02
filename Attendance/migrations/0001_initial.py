# Generated by Django 2.2.5 on 2020-01-02 06:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_status', models.CharField(max_length=10, null=True)),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_attendance', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
