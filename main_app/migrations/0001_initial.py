# Generated by Django 3.0.4 on 2020-04-20 09:04

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
            name='App_functions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function_name', models.CharField(blank=True, max_length=266, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('class_stage', models.CharField(choices=[('Primary', 'Primary'), ('Middle', 'Middle'), ('Highschool', 'Highschool')], max_length=50, null=True)),
                ('class_teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='class_teacher', to=settings.AUTH_USER_MODEL)),
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
                ('session_start_date', models.DateField(blank=True, null=True)),
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
                ('level_name', models.CharField(blank=True, max_length=25, null=True)),
                ('start_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institute_levels', to='main_app.Institute')),
                ('permissions', models.ManyToManyField(blank=True, related_name='user_permissions', to='main_app.App_functions')),
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
                ('roll_number', models.CharField(blank=True, max_length=20, null=True)),
                ('first_name', models.CharField(default='', max_length=25, null=True)),
                ('middle_name', models.CharField(default='', max_length=20, null=True)),
                ('last_name', models.CharField(default='', max_length=25, null=True)),
                ('father_name', models.CharField(default='', max_length=25, null=True)),
                ('mother_name', models.CharField(default='', max_length=25, null=True)),
                ('gender', models.CharField(choices=[('', '-- select one --'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='', max_length=10, null=True)),
                ('date_of_birth', models.DateField(default=datetime.date.today, null=True)),
                ('marital_status', models.CharField(choices=[('', '-- select one --'), ('Married', 'Married'), ('Unmarried', 'Unmarried')], default='', max_length=10, null=True)),
                ('category', models.CharField(choices=[('', '-- select one --'), ('Unreserved', 'Unreserved'), ('Sc/St', 'Sc/St'), ('OBC', 'OBC')], default='', max_length=10, null=True)),
                ('qualification', models.CharField(default='', max_length=200, null=True)),
                ('aadhar_card_number', models.CharField(default='', max_length=20, null=True)),
                ('about', models.CharField(blank=True, default='write something about yourself ', max_length=300, null=True)),
                ('profile_pic', models.ImageField(default='default_profile_pic.jpg', upload_to='UserProfilePictures')),
                ('mobile_number', models.PositiveIntegerField(null=True)),
                ('address_line_1', models.CharField(default='Address line 1', max_length=50, null=True)),
                ('address_line_2', models.CharField(default='Address line 2', max_length=50, null=True)),
                ('city', models.CharField(default='City', max_length=50, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=10, null=True)),
                ('facebook_link', models.URLField(blank=True, default='https://www.facebook.com/', null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approve', 'Approve'), ('dissapprove', 'Dissapprove')], max_length=25, null=True)),
                ('class_promotion_status', models.CharField(choices=[('Promoted', 'Promoted'), ('Not Promoted', 'Not Promoted')], default='Promoted', max_length=30, null=True)),
                ('class_current_year', models.CharField(max_length=30, null=True)),
                ('class_next_year', models.CharField(max_length=30, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('Class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_class', to='main_app.Classes')),
                ('designation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_designation', to='main_app.Institute_levels')),
                ('institute', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='institute', to='main_app.Institute')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.State')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tracking_permission_changes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('changes_made_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_made_changes_permission', to=settings.AUTH_USER_MODEL)),
                ('institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='institute_role_permission_updated', to='main_app.Institute')),
                ('old_permissions', models.ManyToManyField(blank=True, related_name='old_permissions', to='main_app.App_functions')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='role_permission_updated', to='main_app.Institute_levels')),
                ('updated_permissions', models.ManyToManyField(blank=True, related_name='new_permissions', to='main_app.App_functions')),
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
                ('subject_teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subject_teacher', to=settings.AUTH_USER_MODEL)),
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
        migrations.CreateModel(
            name='Institute_disapproved_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('applied_role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.Institute_levels')),
                ('institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institute_disapproved_user', to='main_app.Institute')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disapproved_from', to='main_app.UserProfile')),
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
