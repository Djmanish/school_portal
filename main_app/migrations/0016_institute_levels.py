# Generated by Django 2.2.7 on 2019-11-29 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_auto_20191129_0932'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institute_levels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_name', models.CharField(max_length=25)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institute_levels', to='main_app.Institute')),
            ],
        ),
    ]