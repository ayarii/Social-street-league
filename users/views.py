from email import message
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from users.form import AccountAuthenticationForm, RegistrationForm
from django.conf import settings
from django.http import HttpResponse
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
