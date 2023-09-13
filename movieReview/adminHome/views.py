from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from adminHome.models import Member

# Create your views here.

def index(Request):
    active = "active"
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def dataMG(Request):
    template = loader.get_template('dataMG.html')
    return HttpResponse(template.render())

def reportCM(Request):
    template = loader.get_template('reportCM.html')
    return HttpResponse(template.render())

def dashBD(Request):
    template = loader.get_template('dashBD.html')
    return HttpResponse(template.render())

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