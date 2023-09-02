
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.
def index(request):
    name = "guest"
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def calender(request):
    template = loader.get_template('calender.html')
    return HttpResponse(template.render())

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())