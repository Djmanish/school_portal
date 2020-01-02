# Generated by Django 2.2.5 on 2020-01-02 06:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('class_stage', models.CharField(choices=[('Primary', 'Primary'), ('Middle', 'Middle'), ('Highschool', 'Highschool')], max_length=50, null=True)),
                ('class_teacher', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='class_teacher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=150)),
                ('establish_date', models.DateField(blank=True, null=True)),
                ('profile_pic', models.ImageField(default='default_school_pic.jpg', upload_to='Institute Images')),
                ('principal', models.CharField(max_length=50, null=True)),
                ('contact_number1', models.CharField(max_length=12, null=True)),
                ('contact_number2', models.CharField(blank=True, max_length=12, null=True)),
                ('contact_number3', models.CharField(blank=True, max_length=12, null=True)),
                ('address1', models.CharField(max_length=100, null=True)),
                ('address2', models.CharField(max_length=100, null=True)),
                ('district', models.CharField(max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('about', models.TextField(blank=True, max_length=300, null=True)),
                ('facebook_link', models.URLField(blank=True, default='Facebook Link', null=True)),
                ('website_link', models.URLField(blank=True, default='Website Link', null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institute_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Institute_levels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_id', models.IntegerField(null=True)),
                ('level_name', models.CharField(max_length=25)),
                ('start_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institute_levels', to='main_app.Institute')),
            ],
            options={
                'ordering': ['-level_id'],
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=25, null=True)),
                ('middle_name', models.CharField(default='', max_length=20, null=True)),
                ('last_name', models.CharField(default='', max_length=25, null=True)),
                ('date_of_birth', models.DateField(default=datetime.date.today, null=True)),
                ('about', models.CharField(blank=True, default='write something about yourself ', max_length=300, null=True)),
                ('profile_pic', models.ImageField(default='default_profile_pic.jpg', upload_to='UserProfilePictures')),
                ('mobile_number', models.PositiveIntegerField(default='999999999', null=True)),
                ('address_line_1', models.CharField(default='Address line 1', max_length=50, null=True)),
                ('address_line_2', models.CharField(default='Address line 2', max_length=50, null=True)),
                ('city', models.CharField(default='City', max_length=50, null=True)),
                ('facebook_link', models.URLField(blank=True, default='https://www.facebook.com/', null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approve', 'Approve'), ('dissapprove', 'Dissapprove')], default='pending', max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('Class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='student_class', to='main_app.Classes')),
                ('designation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_designation', to='main_app.Institute_levels')),
                ('institute', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='institute', to='main_app.Institute')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.State')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_code', models.CharField(max_length=100)),
                ('subject_name', models.CharField(max_length=100)),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subject_institute', to='main_app.Institute')),
                ('subject_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='class_subject', to='main_app.Classes')),
            ],
        ),
        migrations.CreateModel(
            name='Role_Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institute_role_desc', to='main_app.Institute')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='level_desc', to='main_app.Institute_levels')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_institute_role', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='institute',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.State'),
        ),
        migrations.AddField(
            model_name='classes',
            name='institute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institute_classes', to='main_app.Institute'),
        ),
    ]
