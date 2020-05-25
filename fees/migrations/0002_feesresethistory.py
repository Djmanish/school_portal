# Generated by Django 3.0.4 on 2020-05-23 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
        ('fees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeesResetHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField(null=True)),
                ('reset_time', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField(null=True)),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.Institute')),
                ('reset_done_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.UserProfile')),
            ],
        ),
    ]
