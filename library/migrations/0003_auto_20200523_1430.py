# Generated by Django 2.2.7 on 2020-05-23 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
        ('library', '0002_auto_20200522_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuebook',
            name='book_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issued_book_name', to='library.Book'),
        ),
        migrations.AlterField(
            model_name='issuebook',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='issuebook',
            name='issued_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issued_by', to='main_app.UserProfile'),
        ),
        migrations.AlterField(
            model_name='issuebook',
            name='user_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_name', to='main_app.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='book',
            unique_together={('book_code', 'book_id', 'book_institute')},
        ),
        migrations.CreateModel(
            name='BookCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, null=True, unique=True)),
                ('book_count', models.IntegerField(null=True)),
                ('book_name', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('publications', models.CharField(max_length=50)),
                ('edition', models.CharField(max_length=50)),
                ('book_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookcode_category', to='library.BookCategory')),
                ('book_institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bookcode_institute', to='main_app.Institute')),
                ('book_sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookcode_sub_category', to='library.BookSubCategory')),
            ],
            options={
                'unique_together': {('code', 'book_institute')},
            },
        ),
    ]
