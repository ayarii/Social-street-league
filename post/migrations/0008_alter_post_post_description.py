# Generated by Django 3.2.15 on 2022-09-01 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_auto_20220829_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_description',
            field=models.TextField(max_length=500),
        ),
    ]
