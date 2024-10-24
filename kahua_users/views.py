from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from django.urls import reverse
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            messages.success(request, 'Registaration successful.')
            return redirect('index')
        else:
            messages.error(request, 'Registration failed.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def log_in(request):
    if 'next' in request.GET:
        messages.info(request, 'Please log in to your Kahua account.')
    if request.method == 'POST':
        form = AuthenticationForm(request, data= request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'login successful.')
            return redirect('index')
        else:
            messages.error(request, 'login failed.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# Create your views here.

def log_out(request):
    auth_logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('kahua_users:login')
