# Generated by Django 3.0.8 on 2020-07-14 04:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='School_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fees_code', models.CharField(max_length=15, null=True)),
                ('description', models.TextField(null=True)),
                ('type', models.CharField(choices=[('debit', 'debit'), ('credit', 'credit')], max_length=7, null=True)),
                ('active', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], max_length=5, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('tax_percentage', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('amount_including_tax', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institute_fees_tags', to='main_app.Institute')),
            ],
            options={
                'unique_together': {('institute', 'fees_code')},
            },
        ),
        migrations.CreateModel(
            name='Transactions_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=20, null=True)),
                ('currency', models.CharField(max_length=10, null=True)),
                ('gateway_name', models.CharField(max_length=20, null=True)),
                ('txnid', models.CharField(max_length=90, null=True)),
                ('BANKTXNID', models.CharField(max_length=90, null=True)),
                ('TXNAMOUNT', models.CharField(max_length=12, null=True)),
                ('STATUS', models.CharField(max_length=25, null=True)),
                ('RESPCODE', models.CharField(max_length=15, null=True)),
                ('RESPMSG', models.TextField(null=True)),
                ('TXNDATE', models.DateTimeField(null=True)),
                ('BANKNAME', models.TextField(null=True)),
                ('PAYMENTMODE', models.CharField(max_length=20, null=True)),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.Institute')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students_all_transactions', to='main_app.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Tags_Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.Institute')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_tags', to='main_app.UserProfile')),
                ('student_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.Classes')),
                ('tags', models.ManyToManyField(related_name='tags_to_student', to='fees.School_tags')),
            ],
        ),
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
        migrations.CreateModel(
            name='Fees_tag_update_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('old_values', models.TextField(null=True)),
                ('new_values', models.TextField(null=True)),
                ('fees_tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags_updates', to='fees.School_tags')),
                ('update_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fees_tag_updates', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fees_Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_date', models.DateField()),
                ('due_date', models.DateField()),
                ('processing_date', models.DateField()),
                ('institute', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='institute_schedule', to='main_app.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='Account_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_id', models.CharField(max_length=25)),
                ('merchant_key', models.CharField(max_length=25)),
                ('institute', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='institute_account_details', to='main_app.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='Students_fees_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField(null=True)),
                ('payment_date', models.DateTimeField(null=True)),
                ('invoice_number', models.CharField(max_length=20, null=True, unique=True)),
                ('total_due_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('total_paid', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('payment_method', models.CharField(max_length=10, null=True)),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.Institute')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='studnts_fees_info', to='main_app.UserProfile')),
                ('student_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.Classes')),
            ],
            options={
                'unique_together': {('institute', 'due_date', 'student')},
            },
        ),
        migrations.CreateModel(
            name='Student_Tag_Processed_Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_date', models.DateField(null=True)),
                ('process_date', models.DateField(null=True)),
                ('due_date', models.DateField(null=True)),
                ('fees_code', models.CharField(max_length=15, null=True)),
                ('description', models.TextField(null=True)),
                ('type', models.CharField(max_length=7, null=True)),
                ('active', models.CharField(max_length=5, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('tax_percentage', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('amount_including_tax', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.Institute')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.UserProfile')),
            ],
            options={
                'unique_together': {('institute', 'due_date', 'student', 'fees_code')},
            },
        ),
    ]
