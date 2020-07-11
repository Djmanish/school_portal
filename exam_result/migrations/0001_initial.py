# Generated by Django 2.1.7 on 2020-07-10 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('examschedule', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalculateResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calc_result_subject', models.CharField(max_length=50, null=True)),
                ('calc_result_exam_type', models.CharField(max_length=50, null=True)),
                ('calc_result_exam_sr_no', models.CharField(max_length=50, null=True)),
                ('calc_result_class', models.CharField(max_length=50, null=True)),
                ('calc_result_score', models.CharField(max_length=100, null=True)),
                ('calc_result_min', models.CharField(max_length=10, null=True)),
                ('calc_result_max', models.CharField(max_length=10, null=True)),
                ('calc_result_total', models.CharField(max_length=10, null=True)),
                ('calc_result_avg', models.CharField(max_length=10, null=True)),
                ('calc_result_student_data', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calc_result_student_data', to=settings.AUTH_USER_MODEL)),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='calc_result_institute', to='main_app.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='ExamResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_sr_no', models.CharField(max_length=100, null=True)),
                ('result_score', models.IntegerField(null=True)),
                ('result_max_marks', models.CharField(max_length=100, null=True)),
                ('exam_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_exam_type', to='examschedule.ExamType')),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_institute', to='main_app.Institute')),
                ('result_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_class', to='main_app.Classes')),
                ('result_student_data', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_student_data', to=settings.AUTH_USER_MODEL)),
                ('result_subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_subject', to='main_app.Subjects')),
                ('result_subject_teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_subject_teacher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Overall_Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_examtype', models.CharField(max_length=50, null=True)),
                ('overall_avg', models.CharField(max_length=50, null=True)),
                ('overall_subject', models.CharField(max_length=50, null=True)),
                ('overall_marks', models.CharField(max_length=50, null=True)),
                ('overall_institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='overall_institute', to='main_app.Institute')),
                ('overall_student_data', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='overall_student_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
