from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(req):
    template = loader.get_template('index.html')
    context = {
        'x': range(5),
    }

    return HttpResponse(template.render(context, req))

def logout(req):

    return HttpResponse("logout")

def login(req):

    return HttpResponse("login")

def register(req):

    return HttpResponse("register")
