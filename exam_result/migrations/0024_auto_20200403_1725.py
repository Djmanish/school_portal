# Generated by Django 2.2.7 on 2020-04-03 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam_result', '0023_auto_20200403_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examresult',
            name='exam_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_exam_type', to='examschedule.ExamType'),
        ),
    ]