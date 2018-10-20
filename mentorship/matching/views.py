from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(req):
    template = loader.get_template('index.html')
    context = {
        'x': range(1),
    }

    return HttpResponse(template.render(context, req))

def testPage(req):
    return render(req, 'loginDemoPage.html', {})

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
            return render(req, 'form.html', {})
    else:
        form = UserCreationForm()

    return render(req, 'register.html', {'form': form})

def userUpdate(req):
    if req.method == 'POST':
        fname = req.POST['first_name']

#        newProfile = Profile(...)

#        newProfile.save()

        print(req.POST)

        return render(req, '', {})

    else:
        return render(req, 'form.html', {})

def userPage(req, user_id):
    # get the page for this user

    return HttpResponse('temp')

def form_view(request):
    form = ProfileForm()
    return render(request, '/form.html', {'form': form})
