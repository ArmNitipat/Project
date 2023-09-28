from imaplib import _Authenticator
from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
#from adminHome.models import myuser
# from .forms import UserForm 
from django.contrib.auth.decorators import login_required


# Create your views here.

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm
from datetime import date

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
            messages.info(request,'Your account has been signup successfully')
            return redirect('home')  # Redirect to a 'home' view, for instance.
    else:
        form = SignupForm()
        return render(request, 'Login_Register/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.info(request,'login successfully')
            return redirect('home')
    return render(request, 'Login_Register/login.html')


def logout_view(request):
    logout(request)
    return redirect('Login_Register/login')


def calculate_age(date_of_birth):
    if date_of_birth:
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        return age
    else:
        return 18 

@login_required
def account(request):
    if request.user.is_authenticated:
        user = request.user  # Get the logged-in user
        user_age = calculate_age(user.date_of_birth)
        context = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'date_of_birth' : user.date_of_birth,
            'user_age': user_age
            if user 
            else None  # Replace with your actual field name
        } 
        return render(request, 'Account/account.html', context)
    else:
        template = loader.get_template('home.html')
        return HttpResponse(template.render())

def update_profile(request):
    if request.method == 'POST':
        # รับข้อมูลจากแบบฟอร์มและอัปเดตข้อมูลผู้ใช้ในฐานข้อมูล
        # เช่น User.objects.filter(username=request.user.username).update(first_name=new_first_name, last_name=new_last_name, email=new_email)
        # โดยให้ new_first_name, new_last_name, และ new_email เป็นค่าที่รับจาก request.POST
        # ตัวอย่างเท่านี้จะขึ้นอยู่กับโครงสร้างของระบบฐานข้อมูลของคุณ

        return redirect('/account')  # หลังจากอัปเดตข้อมูลเรียบร้อยแล้วให้ redirect ไปยังหน้า My account หรือหน้าที่คุณต้องการ

    return render(request, 'settingprofile.html')  # หากเป็น GET request ให้แสดงแบบฟอร์มข้อมูลแก้ไขผู้ใช้

@login_required
def settingprofile(request):
    if request.user.is_authenticated:
        user = request.user  # Get the logged-in user
        user_age = calculate_age(user.date_of_birth)
        context = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'date_of_birth' : user.date_of_birth,
            'user_age': user_age
            if user 
            else None  # Replace with your actual field name
        } 
        return render(request, 'Account/settingprofile.html', context)
    else:
        template = loader.get_template('home.html')
        return HttpResponse(template.render())




def home(request):
    
    if request.user.is_authenticated:
        template = loader.get_template('home.html')
        context = {'username': request.user.username}
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('home.html')
        return HttpResponse(template.render())

def calender(request):
    template = loader.get_template('calender.html')
    return HttpResponse(template.render())

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

# def handleUpdate(request, id):
#     if request.method == "POST":
#         username=request.POST['username']
#         email=request.POST['email']
#         fname=request.POST['fname']
#         lname=request.POST['lname']

#         if len(username)>15:
#             messages.error(request, "Your username must not be more than 15 characters")
#             return redirect('/account') 

#         myuser=User.objects.get(pk=id)
#         myuser.first_name=fname 
#         myuser.last_name=lname
#         myuser.email=email
#         myuser.username=username
#         myuser.save()
#         messages.success(request, "Your account has been updated successfully")
#         return redirect('/account') 