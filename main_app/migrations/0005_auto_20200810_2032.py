# Generated by Django 2.2.7 on 2020-08-10 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20200715_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute',
            name='state',
            field=models.ForeignKey(blank=True, default='Select State', null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.State'),
        ),
    ]