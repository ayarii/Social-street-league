from django.shortcuts import render
from .models import Team
# Create your views here.
def display(request):
    context = {
                'teams':Team.objects.all(),
            }
    return render(request,'team.html',context)