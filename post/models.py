import datetime
from django.db import models
from django.forms import CharField
from location_field.models.plain import PlainLocationField
from SSL.settings import LOCATION_FIELD
from users.models import User

# Create your models here.

class Post(models.Model):
    post_title = models.CharField(max_length=200)
    post_description = models.CharField(max_length=500)
    post_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    post_location = models.CharField(max_length=200)
    #location = PlainLocationField(based_fields=['post_location'],zoom=7, null=True, blank=True)
    post_image = models.ImageField(max_length=255, upload_to='posts_photo/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True, blank=True)
    created_at	= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at= models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.post_title
    def time_ago (self):
        delta = datetime.datetime.now(datetime.timezone.utc) - self.created_at
        d= divmod(delta.seconds, 60)
        h= divmod(delta.seconds, 3600)
        if delta.days :
            return str(delta.days) + " days ago"
        elif h[0] != 0:
            return str(h[0]) + " hours ago"
        elif h[0] == 0 and d[0] != 0 :
            return str(d[0]) + " minutes ago"
        else :
            return "now"
      
        
    
        
    