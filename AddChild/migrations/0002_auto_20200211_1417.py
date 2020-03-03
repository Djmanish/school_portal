# Generated by Django 2.2.5 on 2020-02-11 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AddChild', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addchild',
            name='child',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='main_app.UserProfile'),
        ),
        migrations.AlterField(
            model_name='addchild',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='main_app.UserProfile'),
        ),
    ]