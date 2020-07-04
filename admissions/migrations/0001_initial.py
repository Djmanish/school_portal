# Generated by Django 3.0.8 on 2020-07-02 12:37

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
                ('first_name', models.CharField(max_length=20, null=True, verbose_name='First Name')),
                ('middle_name', models.CharField(blank=True, max_length=20, null=True)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=9, null=True)),
                ('mobile_Number', models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('Email_Id', models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.EmailValidator()])),
                ('student_aadhar_card', models.CharField(default='', max_length=20, null=True)),
                ('student_blood_group', models.CharField(choices=[('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+'), ('A-', 'A-'), ('B-', 'B-'), ('AB-', 'AB-'), ('O-', 'O-')], max_length=9, null=True)),
                ('Address', models.CharField(max_length=100, null=True)),
                ('District', models.CharField(max_length=20, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('Pin_Code', models.IntegerField(null=True)),
                ('p_address', models.CharField(max_length=100, null=True)),
                ('p_district', models.CharField(max_length=20, null=True)),
                ('p_country', models.CharField(blank=True, max_length=100, null=True)),
                ('p_pin_code', models.IntegerField(null=True)),
                ('address_same', models.BooleanField(null=True)),
                ('religion', models.CharField(choices=[('Hindu', 'Hindu'), ('Islam', 'Islam'), ('Sikhs', 'Sikhs'), ('Christain', 'Christain'), ('Bhudhist', 'Bhudhist'), ('Jain', 'Jain'), ('Other', 'Other')], max_length=15, null=True)),
                ('category', models.CharField(choices=[('General', 'General'), ('SC/ST', 'SC/ST'), ('OBC', 'OBC')], max_length=10, null=True)),
                ('sub_cast', models.CharField(blank=True, max_length=100, null=True)),
                ('Student_Photo', models.ImageField(null=True, upload_to='Student_Photos')),
                ('father_name', models.CharField(max_length=30, null=True)),
                ('f_mobile_Number', models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('f_Email_Id', models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.EmailValidator()])),
                ('f_aadhar_card', models.CharField(default='', max_length=20, null=True)),
                ('f_qualification', models.CharField(max_length=20, null=True)),
                ('f_occupation', models.CharField(max_length=20, null=True)),
                ('f_photo', models.ImageField(null=True, upload_to='student_document')),
                ('mother_name', models.CharField(max_length=30, null=True)),
                ('m_mobile_Number', models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('m_Email_Id', models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.EmailValidator()])),
                ('m_aadhar_card', models.CharField(default='', max_length=20, null=True)),
                ('m_qualification', models.CharField(max_length=20, null=True)),
                ('m_occupation', models.CharField(max_length=20, null=True)),
                ('m_photo', models.ImageField(null=True, upload_to='student_document')),
                ('guardian_name', models.CharField(max_length=30, null=True)),
                ('g_mobile_Number', models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')])),
                ('g_Email_Id', models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.EmailValidator()])),
                ('g_aadhar_card', models.CharField(default='', max_length=20, null=True)),
                ('g_qualification', models.CharField(max_length=20, null=True)),
                ('g_occupation', models.CharField(max_length=20, null=True)),
                ('g_photo', models.ImageField(null=True, upload_to='student_document')),
                ('g_applicable', models.BooleanField(null=True)),
                ('dob_certificate', models.FileField(null=True, upload_to='student_document')),
                ('id_proof_certificate', models.FileField(null=True, upload_to='student_document')),
                ('domicile_certificate', models.FileField(null=True, upload_to='student_document')),
                ('cast_certificate', models.FileField(null=True, upload_to='student_document')),
                ('character_certificate', models.FileField(null=True, upload_to='student_document')),
                ('medical_certificate', models.FileField(null=True, upload_to='student_document')),
                ('transfer_certificate', models.FileField(null=True, upload_to='student_document')),
                ('last_year_certificate', models.FileField(null=True, upload_to='student_document')),
                ('class_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requested_school_class', to='main_app.Classes')),
                ('p_State', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ad_p_state', to='main_app.State')),
                ('request_by', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admission_request', to=settings.AUTH_USER_MODEL)),
                ('school_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.Institute')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ad_c_state', to='main_app.State')),
            ],
        ),
    ]
