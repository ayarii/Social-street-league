from django.db import models
from distutils.command import upload
from email.mime import image
from datetime import date, datetime

from activity.models import Activity, Category

# Create your models here.

class Event(models.Model):

    title_event = models.CharField(max_length=50)
    description_event = models.TextField(null = True, blank= True)
    image = models.ImageField(upload_to='photos/%y/%m/%d', default= 'photos/22/07/14')
    affiche = models.ImageField(upload_to='photos/%y/%m/%d',null = True, blank= True)
    location_event = models.CharField(max_length=50)
    date_event = models.DateTimeField(null = True)
    Activity_event = models.ForeignKey(Activity,on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default = datetime.now)


    def __str__(self):
        return self.title_event
    @property
    def event_pass(self):
        return date.today() > self.date_event.date()

    @property
    def event_come(self):
        return date.today() < self.date_event.date()