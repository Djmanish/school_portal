# Generated by Django 2.1.7 on 2020-04-18 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0002_students_fees_table_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students_fees_table',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='studnts_fees_info', to='main_app.UserProfile'),
        ),
    ]
