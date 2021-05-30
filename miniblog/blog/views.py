from django.shortcuts import render,HttpResponseRedirect
from .forms import Signupform,Loginform,Postform
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib.auth.models import Group
# Create your views here.

#home page view
def home(request):
    posts = Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})

#about page
def about(request):
    return render(request,'blog/about.html')    

def contact(request):
    posts=Post.objects.all()
    return render(request,'blog/contact.html',{'posts':posts})     

def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})   
    return render(request,'/login/')       



#signup 
def user_signup(request):
    if request.method=="POST":
        form = Signupform(request.POST)
        if form.is_valid():
            messages.success(request,'congrats!! you become an author')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    form = Signupform()
    return render(request,'blog/signup.html',{'form':form})


#login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form = Loginform(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Logged in suceesfully")
                    return HttpResponseRedirect('/dashboard/') 
        else:
            form = Loginform()
        return render(request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')



#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


#addnewpost
def add_post(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form= Postform(request.POST)
            if form.is_valid():
                form.save()
                form = Postform()
                return HttpResponseRedirect('/dashboard/')
        else:
            form=Postform()
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')    

#updatethepost /edit the post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=Post.objects.get(pk=id)
            form = Postform(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            form=Postform(instance=pi)        
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')         


# delete the post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/') 



