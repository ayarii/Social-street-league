# Generated by Django 3.2.15 on 2022-09-13 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_event_category_event_event_active_event_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='affiche',
            field=models.ImageField(blank=True, null=True, upload_to='photos/%y/%m/%d'),
        ),
    ]
