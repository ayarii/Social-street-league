from django.db import models
from django.forms import CharField

from users.models import User

# Create your models here.

class Post(models.Model):
    post_title = models.CharField(max_length=200)
    post_description = models.CharField(max_length=500)
    post_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    post_location = models.CharField(max_length=200)
    post_image = models.ImageField(max_length=255, upload_to='posts_photo/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True, blank=True)
    def __str__(self):
        return self.post_title
    