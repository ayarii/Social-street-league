from multiprocessing import context
from django.template.loader import render_to_string
from django.http import JsonResponse,HttpResponse
from django.core.mail import EmailMultiAlternatives
import threading
import base64
from django.core.files.base import ContentFile
import uuid
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.views import View
from users.form import AccountAuthenticationForm, AccountUpdateForm, RegistrationForm,ImageUpdateForm
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import account_activation_token
from django.urls import reverse
import os
import json
import base64
from django.core import files
from users.models import Joined_team, User
from post.models import Post, Post_Participants
from team.models import Team
from geopy.geocoders import Nominatim
from geopy.point import Point
from django.contrib.auth.decorators import login_required

# Create your views here.

TEMP_PROFILE_IMAGE_NAME = "default_user.jpg"

class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()
        
def signup_user(request):
    if request.user.is_authenticated:
         return redirect('home')
    username = request.POST.get('username',False)
    email = request.POST.get('email',False) 
    password =request.POST.get('password')
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('activate.html',
                                   {
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': account_activation_token.make_token(user)
                                   }
                                   ).strip()

            email_message = EmailMultiAlternatives(
                'Active your Account',
                message,
                settings.EMAIL_HOST_USER,
                [email]
                )
            email_message.content_subtype = 'html'
            email_message.mixed_subtype = 'related'
            EmailThread(email_message).start()

            return render(request,'activate_mail_done.html')
        else:
            context = {
                'registration_form':RegistrationForm(request.POST),
            }
             
    else:
        form = RegistrationForm()
        context = {
                'registration_form':RegistrationForm(),
            }
        return render(request, 'signup.html', context)
    return render(request, 'signup.html', context)
        
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')
    


def login_user(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if  form.is_valid:
            email=request.POST.get('email')
            password=request.POST.get('password')
            
            user=authenticate(request,email=email,password=password)
            
            if user is not None :
                if user.is_active:
                    login(request,user)
                    if user.is_admin :
                        return redirect('admin:index')
                    else:
                        return redirect('home')
                else:
                    return render(request,'ban.html')
                    
                    
            else:
                messages.info(request,'invalid password or email')
                return redirect('login')
    else:           
        context={'authenticateform':AccountAuthenticationForm()}
        return render(request,'login.html',context)

@login_required(login_url='login')
def logout_user(request,id):
     logout(request)
     return redirect('home')



@login_required(login_url='login')
def profile_user(request, *args, **kwargs):
    geolocator = Nominatim(user_agent="testproject")
    user_id = kwargs.get("id")
    user=User.objects.get(id=user_id)
    context = {}
    context['user']=user
    context['activities']=user.prefer_activity.all()
    context['events']=user.user_events.all()[:2]
    context['teams']=Joined_team.objects.filter(user_id=user_id)[:2]
    context['blogs']=Post.objects.filter(user=user).order_by('-created_at')[:2]
    context['partblogs']=Post_Participants.objects.all().filter(user_id=user)[:2]
    context['postcount']=str(Post.objects.filter(user=user).count())
    context['partpostcount']=str(Post_Participants.objects.all().filter(user_id=user).count())
    context['eventcount']=str(user.user_events.all().count())
    context['teamcount']=str(Joined_team.objects.filter(user_id=user_id).count())
    if not request.user.is_authenticated:
         return redirect("login") 
    account = User.objects.get(id=user_id)
    if account.id != request.user.id:
         return HttpResponse("You cannot edit someone elses profile.")
    
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid(): 
            Latitude = request.POST.get('lat',False)
            Longitude = request.POST.get('long',False)
            location = geolocator.reverse(Point(Latitude , Longitude))
            userr = form.save(commit=False)
            userr.address = location.raw['display_name']
            userr.save()
            return redirect("profile",id=account.id)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
				initial={
					"id": account.id,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"birth_date":account.birth_date,
                    "user_disponibility":account.user_disponibility.all(),
                    "address":account.address,
                    "prefer_activity":account.prefer_activity.all(),
				}
			)
        context['form'] = form
        
    else:
      
        form = AccountUpdateForm(
			initial={
					"id": account.id,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"birth_date":account.birth_date,
                    "user_disponibility":account.user_disponibility.all(),
                    "address":account.address,
                    "prefer_activity":account.prefer_activity.all(),
				}
			)
        context['form'] = form
       
        
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "profile.html", context)
 
 
def upload_image(request,id):
    user=User.objects.get(id=id)
    if request.POST and user.is_authenticated:
        formImage = ImageUpdateForm(request.POST, request.FILES)
        if formImage.is_valid:
            if request.POST.get('base64image',False):
                data = request.POST.get('base64image',False)
                image_array_1 = data.split(";base64,")[1]
                image_array_2 = data.split(";base64,")[0]
                ext=image_array_2.split('/')[1]
                data=ContentFile(base64.b64decode(image_array_1))
                file_name = str(uuid.uuid4()) +"." + ext
                user.profile_image.save(file_name, data, save=True)
                return redirect('profile',id=id)
            else:
                return redirect('profile',id=id)     
    return redirect('profile',id=id)
    
       
            
def filter_data(request):
    dates=request.GET.get('filter')
    id=request.GET.get('id')
    user=User.objects.get(id=id)
    event=user.user_events.all()
    events=[]
    if dates == "Comming Events":
        for e in event:
            if (e.event_come):
                events.append(e)
    elif dates == "Passing Events":
        for e in event:
            if (e.event_pass):
                events.append(e)
    else:
        for e in event:
            events.append(e)
    t=render_to_string('eventsfiltre.html',{'data':events})
    return JsonResponse({'data':t})

def load_more_data_post(request):
    id=request.GET.get('id')
    user=User.objects.get(id=id)
    offset=int(request.GET.get('offset'))
    limit=int(request.GET.get('limit'))
    data=Post.objects.filter(user=user)[offset:offset+limit]
    t=render_to_string('blogsfilter.html',{'data':data})
    return JsonResponse({'data':t}
)
    
def load_more_data_post_part(request):
    id=request.GET.get('id')
    user=User.objects.get(id=id)
    offset=int(request.GET.get('offset'))
    limit=int(request.GET.get('limit'))
    data=Post_Participants.objects.all().filter(user_id=user)[offset:offset+limit]
    t=render_to_string('partblogsfilter.html',{'data':data})
    return JsonResponse({'data':t}
)
    
def load_more_data_event(request):
    id=request.GET.get('id')
    user=User.objects.get(id=id)
    offset=int(request.GET.get('offset'))
    limit=int(request.GET.get('limit'))
    data=user.user_events.all()[offset:offset+limit]
    t=render_to_string('eventsfilter.html',{'data':data})
    return JsonResponse({'data':t}
)
    
def load_more_data_team(request):
    id=request.GET.get('id')
    user=User.objects.get(id=id)
    offset=int(request.GET.get('offset'))
    limit=int(request.GET.get('limit'))
    data=Joined_team.objects.filter(user_id=id)[offset:offset+limit]
    t=render_to_string('teamsfilter.html',{'data':data})
    return JsonResponse({'data':t}
)
    