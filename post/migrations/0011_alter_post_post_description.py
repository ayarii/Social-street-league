# Generated by Django 3.2.15 on 2022-09-03 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_auto_20220901_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_description',
            field=models.TextField(max_length=1000),
        ),
    ]
