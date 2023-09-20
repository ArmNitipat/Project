from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from adminHome.models import myuser
from .forms import UserForm 
# from django.http import JsonResponse

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

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def register(request):
    template = loader.get_template('register.html')
    return HttpResponse(template.render())


# def register(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home_page') # หรือหน้าเว็บที่คุณต้องการไปถัดไป
#     else:
#         form = UserForm()
#     return render(request, 'register.html', {'form': form})


def inuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        
        # ใช้ ORM ของ Django เพื่อบันทึกข้อมูล
        new_entry = myuser(name=username)  # ใส่อายุ 30 หรือค่าอื่นที่คุณต้องการ
        new_entry.save()
        
        # หรือใช้ SQL query โดยตรง (ตัวเลือก)
        # from django.db import connection
        # with connection.cursor() as cursor:
        #     cursor.execute("INSERT INTO my_table (name, age) VALUES (%s, %s)", [username, 30])
        
        return redirect('/')  # หรือ URL อื่นที่คุณต้องการ

    return render(request, 'register.html')  # ใส่ชื่อ template ของคุณ