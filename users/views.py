
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
from users.models import User
from post.models import Post
from geopy.geocoders import Nominatim
from geopy.point import Point
# Create your views here.

TEMP_PROFILE_IMAGE_NAME = "default_user.jpg"

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def signup_user(request):
    if request.user.is_authenticated:
         return redirect('home')
    #username = request.POST.get('username',False)
    #email = request.POST.get('email',False)  
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #user = User.objects.create_user(username=username, email=email)
            form.save()
            # current_site = get_current_site(request)
            # email_body = {
            #         'user': user,
            #         'domain': current_site.domain,
            #         'uid': urlsafe_base64_encode(force_bytes(user.id)),
            #         'token': account_activation_token.make_token(user),
            # }

            # link = reverse('activate', kwargs={
            #                    'uidb64': email_body['uid'], 'token': email_body['token']})

            # email_subject = 'Activate your account'

            # activate_url = 'http://'+current_site.domain+link

            # email = EmailMessage(
            #         email_subject,
            #         'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
            #         'socialstreetleague@gmail.com',
            #         [email],
            #     )
            # EmailThread(email).start()
            # email.send(fail_silently=False)
            # messages.success(request, 'Account successfully created')
            # return render(request, 'signup.html')
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)

            return redirect('home')
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
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'invalid password or email')
                return redirect('login')
    else:           
        context={'authenticateform':AccountAuthenticationForm()}
        return render(request,'login.html',context)

def logout_user(request,id):
     logout(request)
     return redirect('home')

def user(request):
    return render(request,'users.html')

# def profile_user(request,id):
#     user = User.objects.get(id=id)
#     activities=user.prefer_activity.all()
#     context = {
#                 'user':User.objects.get(id=id),
#                 'activities':activities
#             }
#     return render(request,'profile.html',context)


def profile_user(request, *args, **kwargs):
    
    geolocator = Nominatim(user_agent="testproject")
    user_id = kwargs.get("id")
    user=User.objects.get(id=user_id)
    context = {}
    context['user']=user
    context['activities']=user.prefer_activity.all()
    context['events']=user.user_events.all()
    context['teams']=user.user_teams.all()
    context['blogs']=Post.objects.filter(user=user)
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
                    "disponibility":account.disponibility,
                    "address":account.address,
                    
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
                    "disponibility":account.disponibility,
                    "address":account.address,
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
    
            
            