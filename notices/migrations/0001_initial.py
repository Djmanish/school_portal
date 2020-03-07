# Generated by Django 2.1.7 on 2020-03-05 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_app', '0003_auto_20200219_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('publish_date', models.DateTimeField()),
                ('recipients_list', models.ManyToManyField(to='main_app.UserProfile')),
            ],
        ),
    ]
