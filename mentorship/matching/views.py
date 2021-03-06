from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile
from .models import Mentorship

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

        return redirect('userPage', user_id = req.user.id)

    else:
        return render(req, 'form.html', {'hideHeader':True})

def userPage(req, user_id):
    if req.method == 'POST':
        # add default method
        mentor = req.user.profile.getNewMentor()

        # if one was found -- ie, if not none
        if mentor is not None:
            newMentorship = Mentorship.objects.create(mentor = mentor, mentee = req.user)

        req.method = 'GET'

        return redirect('userPage', user_id = user_id)

    else:
        user = get_object_or_404(User, pk=user_id)

        mentees = []
        mentors = []

        for m in user.profile.getAllMentees():
            mentees.append((m, user.profile.getRelationshipStatus(m)))

        for m in user.profile.getAllMentors():
            mentors.append((m, user.profile.getRelationshipStatus(m)))

        return render(req, 'dashboard.html', {'pageUser': user, 'hideHeader' : True, 'mentees' : mentees, 'mentors' : mentors})
