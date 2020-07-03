# Generated by Django 2.1.7 on 2020-07-03 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_code', models.CharField(max_length=20, null=True)),
                ('book_id', models.CharField(max_length=20, null=True)),
                ('book_name', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('publications', models.CharField(max_length=50)),
                ('edition', models.CharField(max_length=50)),
                ('book_count', models.IntegerField(null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=25)),
                ('qr_codes', models.ImageField(blank=True, upload_to='QrCodes')),
            ],
        ),
        migrations.CreateModel(
            name='BookCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_category_name', models.CharField(max_length=50)),
                ('institute_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_institute', to='main_app.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='BookCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, null=True)),
                ('book_count', models.IntegerField(null=True)),
                ('book_name', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('publications', models.CharField(max_length=50)),
                ('edition', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=25)),
                ('book_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookcode_category', to='library.BookCategory')),
                ('book_institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookcode_institute', to='main_app.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='BookSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_sub_category_name', models.CharField(max_length=50)),
                ('institute_subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institute_subcategory', to='main_app.Institute')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='book_sub_category', to='library.BookCategory')),
            ],
        ),
        migrations.CreateModel(
            name='IssueBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issued_date', models.DateTimeField(null=True)),
                ('expiry_date', models.DateTimeField(null=True)),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('delay_counter', models.IntegerField(blank=True, null=True)),
                ('late_fine', models.IntegerField(blank=True, null=True)),
                ('damage_fine', models.IntegerField(default=0)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('book_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='issued_book_name', to='library.Book')),
                ('issue_book_institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issue_book_institute', to='main_app.Institute')),
                ('issued_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issued_by', to='main_app.UserProfile')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_by', to='main_app.UserProfile')),
                ('user_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_name', to='main_app.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='LibrarySettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_Book_Allows', models.IntegerField(blank=True, null=True)),
                ('day_Span', models.IntegerField(blank=True, null=True)),
                ('send_Reminder_Before', models.IntegerField(blank=True, null=True)),
                ('late_fine_per_day', models.IntegerField(blank=True, null=True)),
                ('institute', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='library_settings', to='main_app.Institute')),
            ],
        ),
        migrations.AddField(
            model_name='bookcode',
            name='book_sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookcode_sub_category', to='library.BookSubCategory'),
        ),
        migrations.AddField(
            model_name='book',
            name='book_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='book_category', to='library.BookCategory'),
        ),
        migrations.AddField(
            model_name='book',
            name='book_institute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book_institute', to='main_app.Institute'),
        ),
        migrations.AddField(
            model_name='book',
            name='book_sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='book_sub_category', to='library.BookSubCategory'),
        ),
        migrations.AlterUniqueTogether(
            name='bookcode',
            unique_together={('code', 'book_institute')},
        ),
        migrations.AlterUniqueTogether(
            name='book',
            unique_together={('book_code', 'book_id', 'book_institute')},
        ),
    ]
