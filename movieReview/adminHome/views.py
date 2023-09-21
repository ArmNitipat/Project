from imaplib import _Authenticator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from adminHome.models import myuser
from .forms import UserForm 
# from django.http import JsonResponse

# Create your views here.


def login(request):
    if request.method == "POST":
        Name = request["Name"]
        template = loader.get_template('index.html',Name)
        return HttpResponse(template.render())
    else:
        template = loader.get_template('login.html')
        return HttpResponse(template.render())

def calender(request):
    template = loader.get_template('calender.html')
    return HttpResponse(template.render())

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def register(request):
    template = loader.get_template('register.html')
    return HttpResponse(template.render())

# def signup(request):
#     template = loader.get_template('signup.html')
#     return HttpResponse(template.render())

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = _Authenticator(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserForm()
        return render(request, 'signup.html', {'form': form})
