# Generated by Django 4.0.6 on 2022-07-28 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_alter_team_team_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_about',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]