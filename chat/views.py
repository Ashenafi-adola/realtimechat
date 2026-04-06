from django.shortcuts import render, redirect
from django.views import generic
from . models import Message, CustomUser
from . forms import CustomUserCreationForm, MessageForm
from django.contrib.auth import login, logout, authenticate

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
        print(user)
    context = {
        "page":"signin"
    }
    return render(request, 'chat/authpage.html', context)

def homePage(request):
    users = CustomUser.objects.all()

    context = {
        'users':users
    }
    return render(request, 'chat/home.html', context)

def chatPage(request, pk):
    user = CustomUser.objects.get(id=pk)
    messages = Message.objects.filter(user=user)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = user
            message.save()
            return redirect('home')

    context = {
        'user':user,
        'messages':messages
    }
    return render(request, 'chat/chat.html', context)