from imaplib import _Authenticator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from adminHome.models import myuser
from .forms import UserForm 
#login_required
#from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
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


def signup(request):
    # if request.user.is_authenticated:
    #     return redirect('login')  # ถ้าผู้ใช้เข้าสู่ระบบแล้ว ให้เปลี่ยนเส้นทางไปยังหน้าเข้าสู่ระบบ

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            template = loader.get_template('login.html')
            return HttpResponse(template.render())  # หลังจากการสมัครสมาชิกเสร็จสิ้น ให้เปลี่ยนเส้นทางไปยังหน้าเข้าสู่ระบบ
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserForm()
        return render(request, 'signup.html', {'form': form})

# @login_required
# def protected_view(request):
#     return HttpResponse("You are logged in!")

# def my_view(request):
#     username = request.POST["username"]
#     password = request.POST["password"]
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         template = loader.get_template('/')
#         return HttpResponse(template.render())
#         ...
#     else:
#         # Return an 'invalid login' error message.
#         ...