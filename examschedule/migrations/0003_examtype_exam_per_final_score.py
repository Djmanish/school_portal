# Generated by Django 2.2.7 on 2020-02-12 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examschedule', '0002_auto_20200212_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='examtype',
            name='exam_per_final_score',
            field=models.CharField(max_length=100, null=True),
        ),
    ]