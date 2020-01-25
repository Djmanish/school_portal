# Generated by Django 2.2.7 on 2020-01-23 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20200116_1423'),
        ('examschedule', '0006_auto_20200122_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='examschedule',
            name='Class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='examschedule_class', to='main_app.Classes'),
        ),
    ]
