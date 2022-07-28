from django.shortcuts import render
from .models import Sponsor
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def Display(request):
    sponsor_list = Sponsor.objects.all()
    page = request.GET.get('page', 1)
 
    paginator = Paginator(sponsor_list, 2)
    try:
        sponsors = paginator.page(page)
    except PageNotAnInteger:
        sponsors = paginator.page(1)
    except EmptyPage:
        sponsors = paginator.page(paginator.num_pages)
    return render(request,'sponsor.html' ,{'sp' : sponsors} )