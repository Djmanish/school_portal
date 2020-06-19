# Generated by Django 2.2.7 on 2020-06-19 09:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admission_Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, verbose_name='First Name')),
                ('middle_name', models.CharField(blank=True, max_length=20, null=True)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True)),
                ('father_name', models.CharField(max_length=30, null=True)),
                ('mother_name', models.CharField(max_length=30, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=9, null=True)),
                ('Category', models.CharField(choices=[('General', 'General'), ('sc/st', 'SC/ST'), ('OBC', 'OBC')], max_length=10, null=True)),
                ('mobile_Number', models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('Email_Id', models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.EmailValidator()])),
                ('Nationality', models.CharField(choices=[('Indian', 'Indian'), ('Other', 'Other')], max_length=10, null=True)),
                ('Address', models.CharField(max_length=100, null=True)),
                ('District', models.CharField(max_length=20, null=True)),
                ('Pin_Code', models.IntegerField(null=True)),
                ('Student_Photo', models.ImageField(null=True, upload_to='Student_Photos')),
                ('State', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.State')),
                ('class_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requested_school_class', to='main_app.Classes')),
                ('request_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admission_request', to=settings.AUTH_USER_MODEL)),
                ('school_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admission_request', to='main_app.Institute')),
            ],
        ),
    ]
