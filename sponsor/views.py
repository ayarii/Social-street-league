from django.shortcuts import render
from .models import Sponsor
# Create your views here.


def Display(request):
    return render(request,'sponsor.html' ,{'sp' : Sponsor.objects.all()} )