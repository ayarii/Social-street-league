from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from activity.models import Activity
from event.models import Event

from team.models import Team
# Create your models here.

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to='users_photo', null=True, blank=True, default='users_photo/default_user.jpg')
    age = models.IntegerField(null=True, blank=False)
    disponibility=models.CharField(max_length=50,null=True, blank=False)
    address = models.CharField(max_length=50,null=True, blank=False)
    user_teams = models.ManyToManyField(Team)
    prefer_activity = models.ManyToManyField(Activity)
    user_events = models.ManyToManyField(Event)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.username