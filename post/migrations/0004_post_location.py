# Generated by Django 4.0.6 on 2022-07-28 12:21

from django.db import migrations
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_alter_post_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='location',
            field=location_field.models.plain.PlainLocationField(blank=True, max_length=63, null=True),
        ),
    ]