from django.db import models
from django.db.models import Model

# Create your models here.
class Team(models.Model):
    team_name=models.CharField(max_length=30, unique=True)
    team_about=models.CharField(max_length=400, null=True, blank=True)
    n_players=models.IntegerField()
    team_image = models.ImageField(max_length=255, upload_to='teams_photo', null=True, blank=True, default='teams_photo/default_team.jpg')
    created_at	= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at= models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.team_name
              
        