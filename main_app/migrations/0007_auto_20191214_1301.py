# Generated by Django 2.2.5 on 2019-12-14 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_subjects_institute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjects',
            name='institute',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subject_institute', to='main_app.Institute'),
        ),
    ]