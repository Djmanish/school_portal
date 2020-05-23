# Generated by Django 3.0.4 on 2020-05-21 05:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inst_notice_category', to='main_app.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_no', models.CharField(blank=True, max_length=15, null=True)),
                ('subject', models.CharField(blank=True, max_length=150, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('publish_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_notices', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='notice_category', to='notices.Notification_Category')),
                ('institute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institute_notices', to='main_app.Institute')),
                ('recipients_list', models.ManyToManyField(related_name='users_notice', to='main_app.UserProfile')),
            ],
            options={
                'unique_together': {('reference_no', 'institute')},
            },
        ),
    ]
