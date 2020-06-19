# Generated by Django 2.2.7 on 2020-06-19 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_status', models.CharField(max_length=10, null=True)),
                ('date', models.DateField()),
                ('institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institute_attendance', to='main_app.Institute')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_attendance', to=settings.AUTH_USER_MODEL)),
                ('student_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_class', to='main_app.Classes')),
            ],
        ),
        migrations.CreateModel(
            name='Daily_Attendance_status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_date', models.DateField()),
                ('total_student', models.CharField(max_length=10)),
                ('total_present', models.CharField(max_length=10)),
                ('total_absent', models.CharField(max_length=10)),
                ('total_leave', models.CharField(max_length=10, null=True)),
                ('percentage', models.CharField(max_length=10, null=True)),
                ('attendance_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='daily_class_attendace', to='main_app.Classes')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institute_daily_attendace', to='main_app.Institute')),
            ],
        ),
    ]
