from asyncio.windows_events import NULL
from django.shortcuts import redirect, render
from .models import Team
from users.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def display(request):
    team_list=Team.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(team_list,12)
    try:
        teams = paginator.page(page)
    except PageNotAnInteger:
        teams = paginator.page(1)
    except EmptyPage:
        teams = paginator.page(paginator.num_pages)
    context = {
                'teams':teams,
            }
    return render(request,'team.html',context)

def team_detail(request,id):
    team = Team.objects.get(id=id)
    members=team.user_set.all()
    m=NULL
    
    for i in members:
        if i.id == request.user.id :
            m=i.id
            break
         
    context = {
                'team':Team.objects.get(id=id),
                'members' : members,
                'is_member': User.objects.all().filter(id=m) ,
            }
    return render(request,'singleteam.html',context)


def join_team(request,id):
    team=Team.objects.get(id=id)
    user= User.objects.get(id=request.user.id)
    team.user_set.add(user)
    return redirect('singleteam' , id )

def leave_team(request,id):
    team=Team.objects.get(id=id)
    user= User.objects.get(id=request.user.id)
    team.user_set.remove(user)
    return redirect('singleteam' , id )