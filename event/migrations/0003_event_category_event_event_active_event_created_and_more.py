# Generated by Django 4.0.6 on 2022-08-14 13:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
        ('event', '0002_event_date_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='Category_event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='activity.category'),
        ),
        migrations.AddField(
            model_name='event',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='event',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='event',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]
