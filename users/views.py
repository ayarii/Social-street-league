from email import message
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from users.form import AccountAuthenticationForm, AccountUpdateForm, RegistrationForm
from django.conf import settings
from django.http import HttpResponse

from users.models import User
# Create your views here.

def signup_user(request):
    if request.user.is_authenticated:
         return redirect('home')
         
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
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
        context={'authenticateform':AccountAuthenticationForm()}
        return render(request,'login.html',context)

def logout_user(request,id):
     logout(request)
     return redirect('home')

def user(request):
    return render(request,'users.html')

def profile_user(request,id):
    context = {
                'user':User.objects.get(id=id),
            }
    return render(request,'profile.html',context)


def profile_update(request, *args, **kwargs):
	if not request.user.is_authenticated:
		return redirect("login")
	user_id = kwargs.get("id")
	account = User.objects.get(id=user_id)
	if account.id != request.user.id:
		return HttpResponse("You cannot edit someone elses profile.")
	context = {}
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
					"age":account.age,
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
					"age":account.age,
                    "disponibility":account.disponibility,
                    "address":account.address,
				}
			)
		context['form'] = form
	context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
	return render(request, "updateprofile.html", context)
    
