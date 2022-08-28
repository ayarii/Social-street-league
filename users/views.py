
import threading
import cv2
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.views import View
from users.form import AccountAuthenticationForm, AccountUpdateForm, RegistrationForm
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
            form.save()
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
 
def save_temp_profile_image_from_base64String(imageString, user):
	INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
	try:
		if not os.path.exists(settings.TEMP):
			os.mkdir(settings.TEMP)
		if not os.path.exists(settings.TEMP + "/" + str(user.pk)):
			os.mkdir(settings.TEMP + "/" + str(user.pk))
		url = os.path.join(settings.TEMP + "/" + str(user.pk),TEMP_PROFILE_IMAGE_NAME)
		storage = FileSystemStorage(location=url)
		image = base64.b64decode(imageString)
		with storage.open('', 'wb+') as destination:
			destination.write(image)
			destination.close()
		return url
	except Exception as e:
		print("exception: " + str(e))
		# workaround for an issue I found
		if str(e) == INCORRECT_PADDING_EXCEPTION:
			imageString += "=" * ((4 - len(imageString) % 4) % 4)
			return save_temp_profile_image_from_base64String(imageString, user)
	return None
   
def crop_image(request, *args, **kwargs):
	payload = {}
	user = request.user
	if request.POST and user.is_authenticated:
		try:
			imageString = request.POST.get("profile_image")
			url = save_temp_profile_image_from_base64String(imageString, user)
			img = cv2.imread(url)

			cropX = int(float(str(request.POST.get("cropX"))))
			cropY = int(float(str(request.POST.get("cropY"))))
			cropWidth = int(float(str(request.POST.get("cropWidth"))))
			cropHeight = int(float(str(request.POST.get("cropHeight"))))
			if cropX < 0:
				cropX = 0
			if cropY < 0: # There is a bug with cropperjs. y can be negative.
				cropY = 0
			crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]

			cv2.imwrite(url, crop_img)

			# delete the old image
			user.profile_image.delete()

			# Save the cropped image to user model
			user.profile_image.save("profile_image.png", files.File(open(url, 'rb')))
			user.save()

			payload['result'] = "success"
			payload['cropped_profile_image'] = user.profile_image.url

			# delete temp file
			os.remove(url)
			
		except Exception as e:
			print("exception: " + str(e))
			payload['result'] = "error"
			payload['exception'] = str(e)
	return HttpResponse(json.dumps(payload), content_type="application/json")

