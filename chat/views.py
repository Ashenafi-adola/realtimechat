from django.shortcuts import render, redirect
from django.views import generic
from . models import Message, CustomUser
from . forms import CustomUserCreationForm, MessageForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def signUpPage(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    context = {
        'form':form,
        'page':'signup'
    }
    return render(request, 'chat/authpage.html', context)

def signInPage(request):
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect('home')
    context = {
        "page":"signin"
    }
    return render(request, 'chat/authpage.html', context)

@login_required(login_url='login')
def homePage(request):
    users = CustomUser.objects.all()

    context = {
        'users':users
    }
    return render(request, 'chat/home.html', context)

@login_required(login_url='login')
def chatPage(request, pk):
    user = CustomUser.objects.get(id=pk)
    messages = Message.objects.all()
    form = MessageForm()
    users = CustomUser.objects.all()

    context = {
        'friend':user,
        'messages':messages,
        'form':form,
        'users':users
    }
    return render(request, 'chat/chatroom.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')
