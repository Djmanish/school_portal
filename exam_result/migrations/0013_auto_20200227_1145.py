# Generated by Django 2.2.7 on 2020-02-27 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_result', '0012_auto_20200227_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculateresult',
            name='calc_result_score',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='calculateresult',
            name='calc_result_subject',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
