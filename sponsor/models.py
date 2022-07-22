from django.db import models
from distutils.command import upload
from email.mime import image

# Create your models here.

class Sponsor(models.Model):
    nom_sponsor = models.CharField(max_length=50)
    image = models.ImageField(upload_to='photos/%y/%m/%d', default= 'photos/22/07/14')

    def __str__(self):
        return self.nom_sponsor

