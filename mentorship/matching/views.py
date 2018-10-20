from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

# Create your views here.
def index(req):
    return render(req, 'index.html', {})

def logoutView(req):
    logout(req)

    # TODO add a success message
    return redirect('index')

def register(req):
    if req.user.is_authenticated:
        # TODO: message
        return redirect('')

    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(req, user)
            return render(req, 'form.html', {'hideHeader':True})
    else:
        form = UserCreationForm()

    return render(req, 'register.html', {'form': form,'hideHeader':True})

def userUpdate(req):
    if req.method == 'POST':

        Profile.createFromForm(req)

        return render(req, 'user.html', {'pageUser': req.user, 'hideHeader':True})

    else:
        return render(req, 'form.html', {'hideHeader':True})

def userPage(req, user_id):
    user = get_object_or_404(User, pk=user_id)

    return render(req, 'dashboard.html', {'pageUser': user, 'hideHeader': True})
