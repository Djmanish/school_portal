# Generated by Django 2.2.7 on 2020-02-12 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('examschedule', '0003_examtype_exam_per_final_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examtype',
            old_name='exam_time_number',
            new_name='exam_max_limit',
        ),
    ]