# Generated by Django 2.2.7 on 2020-01-29 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examschedule', '0036_auto_20200129_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examdetails',
            name='exam_subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exam_subject', to='main_app.Subjects'),
        ),
    ]
