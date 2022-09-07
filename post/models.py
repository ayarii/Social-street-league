from asyncio.windows_events import NULL
import datetime
from telnetlib import AUTHENTICATION
from activity.models import Category
from django.db import models
from django.forms import CharField
from location_field.models.plain import PlainLocationField
from users.models import User
# Create your models here.

class Post(models.Model):
    post_title = models.CharField(max_length=200)
    post_description = models.TextField(max_length=1000)
    post_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    post_location = models.CharField(max_length=200)
    lat = models.CharField(max_length=256,null=True,blank=True)
    long = models.CharField(max_length=256,null=True,blank=True)
    post_image = models.ImageField(max_length=255, upload_to='posts_photo/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True, blank=True)
    tags=models.TextField(max_length=1000,null=True,blank=True)
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
    
    def is_participated(self):
        post=Post_Participants.objects.all().filter(post_id=self.id).first()
        m=NULL
        if post :
            participants=post.user_id.all()
            for i in participants:
                if i.is_authenticated:
                    m=i.id
                    break 
            
        return User.objects.all().filter(id=m)
     
    def participants(self):
        np=Post_Participants.objects.all().filter(post_id=self.id).count()
        return np      
    participants = property(participants)   
    
class Post_Participants(models.Model):
    post_id= models.ForeignKey(Post, on_delete=models.CASCADE ,null=True, blank=True)
    user_id= models.ManyToManyField(User)
    
        
    
        
    