from django.db import models
from django.db.models import Model

# Create your models here.
class Team(models.Model):
    team_name=models.CharField(max_length=30, unique=True)
    n_players=models.IntegerField()
    team_image = models.ImageField(max_length=255, upload_to='teams_photo', null=True, blank=True, default='images/default_team.jpg.urls')
    def __str__(self):
        return self.team_name