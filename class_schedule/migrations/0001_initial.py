# Generated by Django 2.1.7 on 2020-05-19 18:17

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
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_stage', models.CharField(choices=[('Primary', 'Primary'), ('Middle', 'Middle'), ('Highschool', 'Highschool')], max_length=50, null=True)),
                ('lecture_name', models.CharField(max_length=100)),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institute_lecture', to='main_app.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], max_length=30)),
                ('Class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedule_class', to='main_app.Classes')),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedule_institute', to='main_app.Institute')),
                ('lecture_eight', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='schedule_lecture_eight', to='class_schedule.Lecture')),
                ('lecture_five', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='schedule_lecture_five', to='class_schedule.Lecture')),
                ('lecture_four', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='schedule_lecture_four', to='class_schedule.Lecture')),
                ('lecture_one', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='schedule_lecture_one', to='class_schedule.Lecture')),
                ('lecture_seven', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='schedule_lecture_seven', to='class_schedule.Lecture')),
                ('lecture_six', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='schedule_lecture_six', to='class_schedule.Lecture')),
                ('lecture_three', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='schedule_lecture_three', to='class_schedule.Lecture')),
                ('lecture_two', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='schedule_lecture_two', to='class_schedule.Lecture')),
                ('subject_lecture_eight', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_lecture_eight', to='main_app.Subjects')),
                ('subject_lecture_five', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_lecture_five', to='main_app.Subjects')),
                ('subject_lecture_four', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_lecture_four', to='main_app.Subjects')),
                ('subject_lecture_one', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_lecture_one', to='main_app.Subjects')),
                ('subject_lecture_seven', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_lecture_seven', to='main_app.Subjects')),
                ('subject_lecture_six', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_lecture_six', to='main_app.Subjects')),
                ('subject_lecture_three', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_lecture_three', to='main_app.Subjects')),
                ('subject_lecture_two', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_lecture_two', to='main_app.Subjects')),
                ('subject_teacher_lecture_eight', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_teacher_lecture_eight', to=settings.AUTH_USER_MODEL)),
                ('subject_teacher_lecture_five', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_teacher_lecture_five', to=settings.AUTH_USER_MODEL)),
                ('subject_teacher_lecture_four', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_teacher_lecture_four', to=settings.AUTH_USER_MODEL)),
                ('subject_teacher_lecture_one', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_teacher_lecture_one', to=settings.AUTH_USER_MODEL)),
                ('subject_teacher_lecture_seven', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_teacher_lecture_seven', to=settings.AUTH_USER_MODEL)),
                ('subject_teacher_lecture_six', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_teacher_lecture_six', to=settings.AUTH_USER_MODEL)),
                ('subject_teacher_lecture_three', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_teacher_lecture_three', to=settings.AUTH_USER_MODEL)),
                ('subject_teacher_lecture_two', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subject_teacher_lecture_two', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
