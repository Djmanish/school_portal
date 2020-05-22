# Generated by Django 2.2.5 on 2020-05-19 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_type_sr_no', models.CharField(max_length=100, null=True)),
                ('exam_type', models.CharField(max_length=100, null=True)),
                ('exam_max_marks', models.CharField(max_length=100, null=True)),
                ('exam_max_limit', models.CharField(max_length=100, null=True)),
                ('exam_per_final_score', models.CharField(max_length=100, null=True)),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='examtype_institute', to='main_app.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='ExamDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_sr_no', models.CharField(max_length=100, null=True)),
                ('exam_code', models.CharField(max_length=100, null=True)),
                ('exam_subject', models.CharField(max_length=100, null=True)),
                ('exam_subject_teacher', models.CharField(max_length=100, null=True)),
                ('exam_date', models.DateField(blank=True, max_length=100, null=True)),
                ('exam_start_time', models.TimeField(max_length=100, null=True)),
                ('exam_end_time', models.TimeField(max_length=100, null=True)),
                ('exam_assign_teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='exam_assign_teacher', to=settings.AUTH_USER_MODEL)),
                ('exam_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='examdetails_class', to='main_app.Classes')),
                ('exam_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exam_type_details', to='examschedule.ExamType')),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='examdetails_institute', to='main_app.Institute')),
            ],
        ),
    ]
