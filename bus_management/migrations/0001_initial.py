# Generated by Django 2.2.7 on 2020-07-22 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_app', '0004_auto_20200715_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_no', models.CharField(max_length=10)),
                ('bus_maker', models.CharField(max_length=15, null=True)),
                ('vehicle_type', models.CharField(max_length=15, null=True)),
                ('fuel_type', models.CharField(max_length=15, null=True)),
                ('bus_color', models.CharField(max_length=10, null=True)),
                ('bus_capacity', models.IntegerField(null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=25)),
                ('bus_institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bus_institute', to='main_app.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_id', models.CharField(max_length=10)),
                ('driving_lic_no', models.CharField(max_length=13)),
                ('institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver_institute', to='main_app.Institute')),
                ('name', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='driver', to='main_app.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_code', models.CharField(max_length=10)),
                ('point_name', models.CharField(max_length=30)),
                ('point_street_no', models.IntegerField(blank=True, null=True)),
                ('point_landmark', models.CharField(max_length=15)),
                ('point_exact_place', models.CharField(blank=True, max_length=20, null=True)),
                ('longitude', models.FloatField(null=True)),
                ('latitude', models.FloatField(null=True)),
                ('point_city', models.CharField(max_length=20)),
                ('point_country', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=25)),
                ('point_institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='point_institute', to='main_app.Institute')),
                ('point_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.State')),
            ],
        ),
        migrations.CreateModel(
            name='RouteInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_no', models.CharField(max_length=20, null=True)),
                ('route_name', models.CharField(max_length=100, null=True)),
                ('from_date', models.DateField(null=True)),
                ('to_date', models.DateField(null=True)),
                ('institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='route_institute', to='main_app.Institute')),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle', to='bus_management.Bus')),
                ('vehicle_driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver', to='bus_management.Driver')),
            ],
        ),
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
        migrations.CreateModel(
            name='RouteMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(default=0)),
                ('time', models.TimeField()),
                ('point', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='point', to='bus_management.Point')),
                ('route', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='route', to='bus_management.RouteInfo')),
                ('routemap_institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='routemap_institute', to='main_app.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='InstituteLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitute', models.FloatField(null=True)),
                ('latitude', models.FloatField(null=True)),
                ('institute', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='transport_institute', to='main_app.Institute')),
            ],
        ),
    ]
