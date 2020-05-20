# Generated by Django 2.2.7 on 2020-05-20 05:53

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
            name='IssueBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issued_by', models.CharField(max_length=50)),
                ('issued_date', models.DateTimeField(null=True)),
                ('expiry_date', models.DateTimeField(null=True)),
                ('return_date', models.DateTimeField(null=True)),
                ('description', models.TextField(blank=True, max_length=100)),
                ('delay_counter', models.IntegerField(null=True)),
                ('book_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issued_book_name', to='library.Book')),
                ('issue_book_institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issue_book_institute', to='main_app.Institute')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_name', to='main_app.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='BookSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_sub_category_name', models.CharField(max_length=50)),
                ('institute_subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institute_subcategory', to='main_app.Institute')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book_sub_category', to='library.BookCategory')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='book_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_category', to='library.BookCategory'),
        ),
        migrations.AddField(
            model_name='book',
            name='book_institute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='book_institute', to='main_app.Institute'),
        ),
        migrations.AddField(
            model_name='book',
            name='book_sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_sub_category', to='library.BookSubCategory'),
        ),
    ]
