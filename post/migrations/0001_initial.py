# Generated by Django 4.0.6 on 2022-07-23 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_user_address_user_age_user_disponibility_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=200)),
                ('post_description', models.CharField(max_length=500)),
                ('post_date', models.DateTimeField()),
                ('post_location', models.CharField(max_length=200)),
                ('post_image', models.ImageField(blank=True, max_length=255, null=True, upload_to='posts_photo')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
    ]
