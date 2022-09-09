from multiprocessing import context
from event.models import Event
from team.models import Team
from post.models import Post
from django.shortcuts import render

# Create your views here.
def home(request):
    events = Event.objects.order_by('-date_event')
    event = events.first()
    posts =Post.objects.all()[0:4]
    posts=sorted (posts, key = lambda p : p.participants, reverse=True)
    context={
        'nextevent':event,
        'events':events[1:4],
        'teams':Team.objects.all()[0:4],
        'blogs':posts,
    }
    return render(request,'home.html',context)

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')