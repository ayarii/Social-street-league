from email import message
from django.contrib.auth import logout
from django.shortcuts import redirect, render

# Create your views here.

def signup_user(request):
    # if request.user.is_authenticated:
    #     return redirect('homepage')
    # else:
    #     form= CreateUserForm()
    #     if request.method == 'POST' :
    #         form=CreateUserForm(request)
    #         if form.is_valid():
    #             form.save()
    #             user = form.cleaned_data.get('username')
    #             message.success(request,'Account created for '+ user)
    #             return redirect('login')
        
        #context={'form':form}
        return render(request,'signup.html')

def login_user(request):
    # if request.user.is_authenticated:
    #     return redirect('homepage')
    # else:
    #     if request.method == 'POST' :
    #         username=request.POST.get('username')
    #         password=request.POST.get('password')
            
    #         user=authenticate(request,username=username,password=password)
            
    #         if user is not None :
    #             login(request,user)
    #             return redirect('homepage')
    #         else:
    #             messages.info(request,'Invalide UserName Or Password')
                
        context={}
        return render(request,'login.html',context)

# def logout_user(request):
#     logout(request)
#     return redirect('login')

def user(request):
    return render(request,'users.html')
