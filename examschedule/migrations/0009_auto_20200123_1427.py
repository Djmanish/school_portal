# Generated by Django 2.2.7 on 2020-01-23 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examschedule', '0008_remove_examschedule_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examschedule',
            name='test_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_class', to='main_app.Classes'),
        ),
        migrations.AlterField(
            model_name='examschedule',
            name='test_subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_subject', to='main_app.Subjects'),
        ),
    ]
