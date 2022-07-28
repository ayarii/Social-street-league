from asyncio.windows_events import NULL
from django.shortcuts import redirect, render
from .models import Team
from users.models import User
# Create your views here.
def display(request):
    context = {
                'teams':Team.objects.all(),
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