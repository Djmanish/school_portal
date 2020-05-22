# Generated by Django 2.2.5 on 2020-05-22 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0009_auto_20200522_0949'),
    ]

    operations = [
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
    ]
