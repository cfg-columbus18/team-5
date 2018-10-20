from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(req):
    template = loader.get_template('index.html')
    context = {
        'x': range(5),
    }

    return HttpResponse(template.render(context, req))

def logoutView(req):

    return HttpResponse("logout")

def loginPage(req):

    return HttpResponse("login")

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
