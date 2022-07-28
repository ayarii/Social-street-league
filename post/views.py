from django.shortcuts import redirect, render

from post.form import post_form
from post.models import Post

# Create your views here.
def display(request):
    context = {
                'posts':Post.objects.all(),
            }
    return render(request,'post.html',context)

def add_post(request):
    
    if request.method == 'POST':
        form = post_form(request.POST, request.FILES)
        if  form.is_valid:
            post = form.save(commit=False)
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

def update_post(request,id):
    post= Post.objects.get(id=id)
    if request.method == 'POST':
        form = post_form(request.POST,request.FILES,instance=post)
        if  form.is_valid:
            form.save()
            return redirect('post')
    else:
        form = post_form(instance=post)
       
    context = {
                'form':form,
            }
    return render(request,'updatepost.html',context)
  
def delete_post(request,id):
    post= Post.objects.get(id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('post') 
    
   