from asyncio.windows_events import NULL
import email
from django.http import JsonResponse
import os
import string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from .models import Team
from users.models import Joined_team, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from email.mime.image import MIMEImage
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
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
    #team = Joined_team.objects.filter(team_id=id)
    members= Joined_team.objects.filter(team_id=id)
    is_member = Joined_team.objects.filter(team_id=id).filter(user_id=request.user.id)
    m=NULL
    if is_member :
        if is_member[0].is_approved :  
            m=True
        else:
            m=False
                           
    context = {
                'team':Team.objects.get(id=id),
                'members' : members,
                'is_member': is_member,
                'is_approved' :m,
            }
    
    return render(request,'singleteam.html',context)

@login_required(login_url='login')
def join_team(request,id):
    team=Team.objects.get(id=id)
    user= User.objects.get(id=request.user.id)
    user_team= Joined_team()
    user_team.user=user
    user_team.team=team
    user_team.save()
    current_site = get_current_site(request)

    admin_list=User.objects.filter(is_admin=True)
    admin_emails=[]
    for i in admin_list:
        admin_emails.append(i.email)    
    text_content=render_to_string("join_team_email.html",{"team":team,"user":user,"domain":current_site.domain}).strip()
    email = EmailMultiAlternatives(
        #subject
        "A New request for Join_Team",
        #content
        text_content,
        #from email,
        settings.EMAIL_HOST_USER,
        #to list
        admin_emails
    )
    email.content_subtype = 'html'
    email.mixed_subtype = 'related'
    email.send()
    return redirect('singleteam', id )

def leave_team(request,id):
    team= Joined_team.objects.filter(team_id=id).filter(user_id=request.user.id)
    team.delete()
    return redirect('singleteam' , id )

# class InfoListView(ListView):
#     model = Team
#     template_name = 'team.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["qs_json"] = json.dumps(list(Team.objects.values('team_name','n_players','team_image')))
#         return context

def Search_ajax(request):
    if request.is_ajax():
        res=None
        team=request.POST.get('team')
        type=request.POST.get('type')
        if len(team) <= 0:
            if type == "profile":
                res=Joined_team.objects.filter(user_id=request.user.id)
            else:
                res=Team.objects.all().filter(team_name=team)
                 
        if type == "profile":
            qs=Joined_team.objects.filter(user_id=request.user.id)
            if len(qs) > 0 and len(team) > 0:
                data =[]
                for pos in qs:
                    if pos.team.team_name == team :
                        item ={
                                'id' : pos.id,
                                'team_name':pos.team.team_name,
                                'n_players':pos.team.n_players,
                                'team_image':str(pos.team.team_image.url),
                                'status':'leave'
                            }
                        data.append(item)
                res=data
            else:
                res = 'No results found...'
          
            return JsonResponse({'data':res})
        else:
            if len(team) > 0 :
                qs=Team.objects.all().filter(team_name=team)
            else:
               qs=Team.objects.all()
            
            if len(qs) > 0 :
                data =[]
                for pos in qs:
                    item ={
                        'id' : pos.id,
                        'team_name':pos.team_name,
                        'n_players':pos.n_players,
                        'team_image':str(pos.team_image.url),
                        'status':'join'
                    }
                    data.append(item)
                res=data
            else:
                res = 'No results found...'
        
            return JsonResponse({'data':res})
    return JsonResponse({})