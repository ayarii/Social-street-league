from difflib import context_diff
from django.shortcuts import render
from .models import Event
from django.core.paginator import Paginator
# Create your views here.

#def Display(request):
    #return render(request,'event.html' ,{'ev' : Event.objects.all()} )

def list_event(request):
    event_list = Event.objects.all()

    p = Paginator(event_list, 3)
    page = request.GET.get('page')
    events = p.get_page(page)
    nums = "a" * events.paginator.num_pages


    context = {'event_list': event_list,
    'events': events,
    'nums': nums}
    return render(request,'event.html',context
     )

def even(request, id):
    obj = Event.objects.get(id = id)
    context = {
        #'title': obj.title_event,
        #'descrition ': obj.description_event,
        #'image': obj.image,
        #'location': obj.location_event,
        #'date': obj.date_event,
        #'Activity': obj.Activity_event

        'object': obj
    }
    return render(request,'even.html', context
     )
