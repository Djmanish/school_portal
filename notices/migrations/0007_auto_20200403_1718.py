# Generated by Django 2.2.7 on 2020-04-03 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0006_notice_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='recipients_list',
            field=models.ManyToManyField(related_name='users_notice', to='main_app.UserProfile'),
        ),
    ]