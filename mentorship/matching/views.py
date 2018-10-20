from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(req):
    template = loader.get_template('index.html')
    context = {
        'x': range(5),
    }

    return HttpResponse(template.render(context, req))

def logoutView(req):
    logout(req)

    # TODO add a success message
    return redirect('index')

def register(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(req, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(req, 'register.html', {'form': form})

def userPage(req, user_id):
    # get the page for this user

    return HttpResponse('temp')
