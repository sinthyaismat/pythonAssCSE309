from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.models import User
from . import models
# Create your views here.
def home(request):
    post=models.post.objects.all().order_by('-id')
    context={
        'posts':post,
    }
    return render(request,"index.html",context)
def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['uname']
            pass1 = request.POST['psw']
            pass2 = request.POST['psw-repeat']
            if pass1 != pass2:
                messages.error(request,"Password didn't match!")
            else:
                myuser = User.objects.create_user(username=username, password=pass1)
                myuser.is_active=True
                myuser.save()
                return redirect('/login')
        return render(request,"signup.html")
    else:
        return redirect('/')
def loggin(request):
    if not request.user.is_authenticated:      
        if request.method == 'POST':  
            username = request.POST['uname']
            pass1 = request.POST['psw']
            user = authenticate(username=username, password=pass1)

            if user is not None:   
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Bad Credentials!")
                return redirect('/')

        return render(request,"login.html")
    else:
        return redirect('/')
def loggout(request):
    logout(request)
    return redirect('/')
def mypost(request):
    if request.user.is_authenticated:
        posts=models.post.objects.filter(uid=request.user)
        context={

            'posts':posts,
        }
        return render(request,"mypost.html",context)
    else:
        return redirect('/')

def newpost(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            title=request.POST['btitle']
            des=request.POST['des']
            # print(request.user.id,title,des)
            post= models.post(uid=request.user,tital=title,des=des)
            post.save()
            return redirect('/mypost')
        return render(request, "newpost.html")
    else:
        return redirect('/')

def update(request, idup):
    if request.user.is_authenticated:
        post=models.post.objects.get(id=idup,uid=request.user)
        if post is not None:

            context={
                'post':post,
            }

            if request.method=='POST':
                post.tital=request.POST['btitle']
                post.des=request.POST['des']
                post.save()
                return redirect('/mypost')
            return render(request,"update.html",context)

        else:
            return redirect('/')
    else:
        return redirect('/')    
def delete(request, idde):
    if request.user.is_authenticated:
        post=models.post.objects.get(id=idde,uid=request.user)
        print(post)
        if post is not None:

            context={
                'post':post,
            }
            if request.method=='POST':
                post.delete()
                return redirect('/mypost')
            return render(request,"delete.html",context)
        else:
            return redirect('/')
    else:
        return redirect('/')