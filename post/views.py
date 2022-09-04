from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from post.form import post_form
from post.models import Post, Post_Participants 
from users.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from geopy.geocoders import Nominatim
from geopy.point import Point
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
# Create your views here.
def display(request):
    post_list=Post.objects.all().order_by('-created_at')

    page = request.GET.get('page', 1)
    paginator = Paginator(post_list,5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
                'posts':posts,
            }
    return render(request,'post.html',context)

@login_required(login_url='login')
def add_post(request):
    geolocator = Nominatim(user_agent="testproject")
    if request.method == 'POST':
        form = post_form(request.POST, request.FILES)
        if  form.is_valid:
            Latitude = request.POST.get('lat',False)
            Longitude = request.POST.get('long',False)
            location = geolocator.reverse(Point(Latitude , Longitude))
            post = form.save(commit=False)
            post.post_location = location.raw['display_name']
            post.user = request.user
            post.save()
            return redirect('post')
    else:
        context = {
                'form':post_form(),
            }
        return render(request,'addpost.html',context)
    context = {
                'form':post_form(),
            }
    return render(request,'addpost.html',context)

@login_required(login_url='login')
def update_post(request,id):
    geolocator = Nominatim(user_agent="testproject")
    post= Post.objects.get(id=id)
    if request.method == 'POST':
        form = post_form(request.POST,request.FILES,instance=post)
        if  form.is_valid:
            Latitude = request.POST.get('lat',False)
            Longitude = request.POST.get('long',False)
            location = geolocator.reverse(Point(Latitude , Longitude))
            posts = form.save(commit=False)
            posts.post_location = location.raw['display_name']
            posts.save()
            return redirect('post')
    else:
        form = post_form(instance=post)
       
    context = {
                'form':form,
            }
    return render(request,'updatepost.html',context)

@login_required(login_url='login') 
def delete_post(request,id):
    Post.objects.get(id=id).delete()
    return redirect ('post')

@login_required(login_url='login') 
def participate_post(request):
    user=User.objects.get(id=request.user.id)
    id=request.GET.get('id_p')
    pp=Post_Participants()
    pp.post_id=Post.objects.get(id=id)
    pp.save()
    pp.user_id.add(user)
    pp.save()
    post_list=Post.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list,5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    t=render_to_string('post.html',{'posts':posts})
    return JsonResponse({'posts':t})
    

          
    

    
    

   