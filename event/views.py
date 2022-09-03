from difflib import context_diff
import email
from http.client import HTTPResponse
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render, redirect
from .models import Event,Activity, Category
from django.core.paginator import Paginator
import folium
from .forms import EventForm
from django.core.mail import send_mail


from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

#def Display(request):
    #return render(request,'event.html' ,{'ev' : Event.objects.all()} )
def contact(request):
    if request.method== "POST":
         message_name = request .POST['name']
         message_email = request.POST['email']
         message = request.POST['message']

         #send an email

         send_mail(
            message_name,
            message,
            message_email,
            email='email',
        
         )

         return render(request, 'contact.html', {'name': message_name})
    else:
        return render (request, 'contact.html', {})

def event_pdf(request):
    #Create Bytestream buffer
    buf = io.BytesIO()
    #Create a canvas
    c= canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    #Add some lines of text
    #lines = [
        #"This is line 1",
        #"This is line 2 ",
        #"This is line 3",
    #]

    event_pdf= Event.objects.all()
    lines = []

    for event in event_pdf:
        lines .append(event.title_event)
       


    #loop
    for line in lines:
        textob.textLine(line)

    #Finish Up
    c.drawText(textob)
    c.showPage()
    c.save
    buf.seek(0)

    #Return something
    return FileResponse(buf, as_attachment=True, filename='event_pdf')



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

def eve(request):
    eve = Event.objects.filter('Category_event')

    context = {
        'eve':eve
    }
    return render(request,'eve.html',context
     )

def list_event(request):
    event_list = Event.objects.all()
    allevents = Event.objects.filter(active=True).count()

    p = Paginator(event_list, 3)
    page = request.GET.get('page')
    events = p.get_page(page)
    nums = "a" * events.paginator.num_pages


    context = {'event_list': event_list,
    'events': events,
    'nums': nums,
    'allevents':allevents,
    'category': Category.objects.all(),}
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

def updatev(request, id):
    event_id = Event.objects.get(id = id)
    if request.method == 'POST':
        event_save = EventForm(request.POST, request.FILES, instance=event_id)
        if event_save.is_valid():
            event_save.save()
    else:
        event_save = EventForm(instance=event_id)
    context = {
        'form':event_save,
    }
    return render(request, 'event/updatev.html', context)


