# Generated by Django 4.0.6 on 2022-07-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=30, unique=True)),
                ('n_players', models.IntegerField()),
                ('team_image', models.ImageField(blank=True, default='images/default_team.jpg.urls', max_length=255, null=True, upload_to='teams_photo')),
            ],
        ),
    ]
