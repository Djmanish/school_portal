# Generated by Django 2.2.5 on 2020-07-15 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bus_management', '0002_routemap'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('date', models.DateField()),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trip_driver', to='bus_management.Driver')),
                ('point', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bus_management.Point')),
                ('route', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trip_route', to='bus_management.RouteInfo')),
            ],
        ),
    ]
