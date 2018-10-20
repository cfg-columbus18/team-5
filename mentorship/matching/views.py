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

def addDefaultMentor(req):
    mentor = req.user.profile.getNewMentor()

    addMentor(req, mentor)

def addMentor(req,mentor):
    newMentorship = Mentorship.objects.create(mentor = mentor, mentee = req.user)

    # TODO:  users page
    return userPage(req, req.user.id)

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
            return render(req, 'form.html', {})
    else:
        form = UserCreationForm()

    return render(req, 'register.html', {'form': form})

def userUpdate(req):
    if req.method == 'POST':
        Profile.createFromForm(req)

        return render(req, 'dashboard.html', {'pageUser': req.user})

    else:
        return render(req, 'form.html', {})

def userPage(req, user_id):
    user = get_object_or_404(User, pk=user_id)

    mentees = []
    mentors = []

    for m in user.profile.getAllMentees():
        mentees.append((m, user.profile.getRelationshipStatus(m)))

    for m in user.profile.getAllMentors():
        mentors.append((m, user.profile.getRelationshipStatus(m)))

    print(len(mentors))

    for i in mentors:
        print(i[0])
        print('goal' == i[0])
        print(type(i[0]) is User)
        print(type(i[0]) is Profile)
    for i in mentees:
        print(i[0])
        print('goal' == i[0])
        print(type(i[0]) is User)
        print(type(i[0]) is Profile)

    return render(req, 'dashboard.html', {'pageUser': user, 'hideHeader' : True, 'mentees' : mentees, 'mentors' : mentors})
