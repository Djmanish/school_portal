# Generated by Django 2.2.7 on 2020-02-26 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_result', '0010_examresult_result_max_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examresult',
            name='result_max_marks',
            field=models.CharField(max_length=100, null=True),
        ),
    ]