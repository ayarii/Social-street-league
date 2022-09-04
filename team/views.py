from asyncio.windows_events import NULL
import email
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