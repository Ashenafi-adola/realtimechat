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
            return redirect('home')
    context = {
        'form':form,
    }
    return render(request, 'chat/authpage.html', context)

def signInPage(request):
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username, password)
        if user != None:
            return redirect('home')
    context = {

    }
    return render(request, 'chat/authpage.html', context)