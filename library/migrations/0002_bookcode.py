# Generated by Django 2.2.5 on 2020-05-20 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_remove_userprofile_country'),
        ('library', '0001_initial'),
    ]

    operations = [
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
                ('book_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookcode_category', to='library.BookCategory')),
                ('book_institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bookcode_institute', to='main_app.Institute')),
                ('book_sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookcode_sub_category', to='library.BookSubCategory')),
            ],
        ),
    ]
