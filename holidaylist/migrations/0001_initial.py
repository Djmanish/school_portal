# Generated by Django 2.2.7 on 2020-06-19 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HolidayList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(max_length=100, null=True)),
                ('days', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10, null=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('applicable', models.CharField(choices=[('No', 'No'), ('Yes', 'Yes')], max_length=10, null=True)),
                ('holiday_type', models.CharField(max_length=100, null=True)),
                ('holiday_email', models.CharField(choices=[('No', 'No'), ('Yes', 'Yes')], max_length=10, null=True)),
                ('holiday_sms', models.CharField(choices=[('No', 'No'), ('Yes', 'Yes')], max_length=10, null=True)),
                ('holiday_notification', models.CharField(choices=[('No', 'No'), ('Yes', 'Yes')], max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='holiday_institute', to='main_app.Institute')),
            ],
        ),
    ]
