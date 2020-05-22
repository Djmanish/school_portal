# Generated by Django 2.2.5 on 2020-05-19 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecondryInstitute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_rollno', models.IntegerField(null=True)),
                ('institute_type', models.CharField(choices=[('primary', 'primary'), ('secondry', 'secondry')], default='secondry', max_length=9)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('active', 'active')], default='pending', max_length=9)),
                ('student_Class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='student_Class', to='main_app.Classes')),
                ('student_institute', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='student_institute', to='main_app.Institute')),
                ('student_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_name', to='main_app.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='AddChild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('active', 'active')], default='pending', max_length=9)),
                ('Class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='stu_class', to='main_app.Classes')),
                ('child', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='main_app.UserProfile')),
                ('institute', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='studnt_institute', to='main_app.Institute')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='main_app.UserProfile')),
            ],
        ),
    ]
