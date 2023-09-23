from imaplib import _Authenticator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
#from adminHome.models import myuser
from .forms import UserForm 


# Create your views here.

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm



# from django.shortcuts import render, redirect
# from .forms import SignupForm

# def signup_view(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Here, you can save any additional data or perform other operations as required
#             return redirect('login')  # or redirect to some other page
#     else:
#         form = SignupForm()
#     return render(request, 'your_template_name.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a 'home' view, for instance.
    else:
        # form = UserForm()
        form = SignupForm()
        return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')




def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def calender(request):
    template = loader.get_template('calender.html')
    return HttpResponse(template.render())

# def login(request):
#     template = loader.get_template('login.html')
#     return HttpResponse(template.render())

def register(request):
    # if request.user.is_authenticated:
    #     print(request.user.is_authenticated)
    #     return redirect('login')  # ถ้าผู้ใช้เข้าสู่ระบบแล้ว ให้เปลี่ยนเส้นทางไปยังหน้าเข้าสู่ระบบ

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # template = loader.get_template('login.html')
            # return HttpResponse(template.render())  # หลังจากการสมัครสมาชิกเสร็จสิ้น ให้เปลี่ยนเส้นทางไปยังหน้าเข้าสู่ระบบ
            return redirect('login') 
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'register.html', {'form': form})

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