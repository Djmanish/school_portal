# Generated by Django 2.2.7 on 2020-02-12 05:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
        ('examschedule', '0001_initial'),
        ('exam_result', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='examresult',
            name='result_exam_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_exam_code', to='examschedule.ExamDetails'),
        ),
        migrations.AddField(
            model_name='examresult',
            name='result_student_data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_student_data', to='main_app.UserProfile'),
        ),
        migrations.AddField(
            model_name='examresult',
            name='result_subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_subject', to='main_app.Subjects'),
        ),
        migrations.AddField(
            model_name='examresult',
            name='result_subject_teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_subject_teacher', to=settings.AUTH_USER_MODEL),
        ),
    ]
