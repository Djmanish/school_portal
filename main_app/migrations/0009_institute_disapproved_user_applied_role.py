# Generated by Django 2.1.7 on 2020-04-09 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_institute_disapproved_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute_disapproved_user',
            name='applied_role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.Role_Description'),
        ),
    ]