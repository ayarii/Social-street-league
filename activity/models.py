from unicodedata import category
from django.db import models
from distutils.command import upload

# Create your models here.

class Category(models.Model):
   
    category_name = models.CharField(max_length=50)
   

    def __str__(self):
        return self.category_name

class Activity(models.Model):

    title_activity = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default = 1)
    def __str__(self):
        return self.title_activity