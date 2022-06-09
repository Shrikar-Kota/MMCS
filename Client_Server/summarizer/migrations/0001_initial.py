# Generated by Django 3.2.12 on 2022-05-30 05:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.TextField()),
                ('uploaddate', models.DateTimeField()),
                ('filetype', models.CharField(max_length=6)),
                ('fileextension', models.CharField(max_length=6)),
                ('fileid', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('start_time_of_media', models.IntegerField()),
                ('end_time_of_media', models.IntegerField()),
                ('total_duration_of_media', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
