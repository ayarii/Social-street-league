from difflib import context_diff
from django.shortcuts import render, redirect
from .models import Event
from django.core.paginator import Paginator
from .forms import EventForm
# Create your views here.

#def Display(request):
    #return render(request,'event.html' ,{'ev' : Event.objects.all()} )
def addev(request):

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if  form.is_valid():
            form.save()
            return redirect ('/addev?submitted=True')
        else:
            context = {
                'form': EventForm,
            }
        return render(request,'addev.html',context)
    context = {
                'form': EventForm,
            }
    return render(request,'addev.html',context)

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
