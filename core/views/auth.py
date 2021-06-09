from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from users.models import User

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_url = "/player/main/"
            if user.role == 2:
                redirect_url = "/coach/main/"
            return redirect(redirect_url)
        else:
            return render(request, 'auth/login.html', {
                'redirect_url': "",
                'error': 'Invalid credentials'
            })
    else:
        if request.user.is_authenticated:
            if request.user.role == 2:
                return redirect('coach_main')
            else:
                return redirect('player_main')
        redirect_url = request.GET.get('redirect_url')
        return render(request, 'auth/login.html', { 'redirect_url': redirect_url or "" })

def signout(request):
    logout(request)
    return redirect("/")