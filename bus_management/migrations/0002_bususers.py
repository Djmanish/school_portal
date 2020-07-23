# Generated by Django 2.2.7 on 2020-07-22 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20200715_1531'),
        ('bus_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_institute', to='main_app.Institute')),
                ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus_management.Point')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bus_users', to='main_app.UserProfile')),
            ],
        ),
    ]
