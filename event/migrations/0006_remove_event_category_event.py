# Generated by Django 3.2.15 on 2022-09-13 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_auto_20220913_1748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='Category_event',
        ),
    ]
