# Generated by Django 2.2.7 on 2020-02-20 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examschedule', '0005_examtype_exam_type_sr_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examdetails',
            name='exam_sr_no',
        ),
        migrations.RemoveField(
            model_name='examdetails',
            name='exam_type',
        ),
        migrations.CreateModel(
            name='ExamCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_sr_no', models.CharField(max_length=100, null=True)),
                ('exam_code', models.CharField(max_length=100, null=True)),
                ('exam_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exam_type_details', to='examschedule.ExamType')),
            ],
        ),
    ]
