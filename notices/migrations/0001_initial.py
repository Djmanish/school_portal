# Generated by Django 2.1.7 on 2020-04-18 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_no', models.CharField(blank=True, max_length=15, null=True)),
                ('subject', models.CharField(max_length=150)),
                ('content', models.TextField()),
                ('publish_date', models.DateTimeField()),
                ('category', models.CharField(blank=True, choices=[('absent', 'absent')], max_length=15, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_notices', to=settings.AUTH_USER_MODEL)),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institute_notices', to='main_app.Institute')),
                ('recipients_list', models.ManyToManyField(related_name='users_notice', to='main_app.UserProfile')),
            ],
        ),
    ]
