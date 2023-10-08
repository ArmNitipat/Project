from imaplib import _Authenticator
from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
#from adminHome.models import myuser
# from .forms import UserForm 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
# from .forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm
from datetime import date
from django.contrib.auth import update_session_auth_hash
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

@login_required
def update_user(request):
    if request.method == 'POST':
        # รับข้อมูลจาก POST request
        new_firstname = request.POST.get('firstname')
        new_lastname = request.POST.get('lastname')
        new_email = request.POST.get('email')
        new_image = request.FILES.get('profile_image')

        # อัปเดตข้อมูลผู้ใช้ในฐานข้อมูล
        user = request.user
        user.first_name = new_firstname
        user.last_name = new_lastname
        user.email = new_email
        user.save()
        
        # ถ้ามีรูปภาพเก่าในโมเดล, ลบมัน
        if new_image:
            if user.image:
                user.image.delete(save=False)
            user.image = new_image
            user.save()
        messages.success(request, 'ข้อมูลของคุณถูกอัปเดตแล้ว')
        return redirect('settingprofile')  # ลิงก์ไปยังหน้าโปรไฟล์หลังจากอัปเดตข้อมูล
    return redirect('account')


@login_required
def get_user_data(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        return JsonResponse(user_data)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if not user.image:
                user.image = 'profile_images/istockphoto612x612.jpg' 
                user.save()
            login(request, user)
            return redirect('home')  # Redirect to a 'home' view, for instance.
    else:
        form = SignupForm()
    return render(request, 'Login_Register/register.html', {'form': form}) #form จะถูกหรือไม่ view จะส่งกลับ HttpResponse ในทุกสถานการณ์.


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            context['login_error'] = "This username and email could not be found."
    return render(request, 'Login_Register/login.html', context)




def resetpassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        # ตรวจสอบว่ามีผู้ใช้ที่ตรงกับ username และ email ในฐานข้อมูลหรือไม่
        user = User.objects.filter(username=username, email=email).exists()
        if user:
            # ถ้าผ่านการตรวจสอบ, ไปที่หน้า resetpassword2
            return redirect(user,'resetpassword2')
        else:
            messages.error(request, 'ไม่พบผู้ใช้ที่มีชื่อผู้ใช้และอีเมลนี้')
            return render(request, 'Login_Register/resetpassword.html')

    return render(request, 'Login_Register/resetpassword.html')

def check_credentials(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')

        try:
            user = User.objects.get(username=username, email=email)
            # User found, redirect to the password reset page and store user_id in the session
            request.session['user_id_for_reset'] = user.id
            # messages.success(request, 'User found, please reset your password!')
            return redirect('resetpassword')
        except User.DoesNotExist:
            messages.error(request, 'No user found with provided username and email.')
            return redirect('credentials')

    return render(request, 'Login_Register/credentials.html')


from django.contrib.auth.forms import SetPasswordForm
def reset_password(request):
    user_id = request.session.get('user_id_for_reset')
    if user_id is not None:
        user = User.objects.get(id=user_id)
        
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = SetPasswordForm(user)

        return render(request, 'Login_Register/resetpassword.html', {'form': form})

    else:
        messages.error(request, 'No reset request found. Please submit your username and email again.')
        return redirect('credentials')



def logout_view(request):
    logout(request)
    return redirect('login')


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

#เตรียมลบ
# def update_profile(request):
#         # รับข้อมูลจากแบบฟอร์มและอัปเดตข้อมูลผู้ใช้ในฐานข้อมูล
#         # เช่น User.objects.filter(username=request.user.username).update(first_name=new_first_name, last_name=new_last_name, email=new_email)
#         # โดยให้ new_first_name, new_last_name, และ new_email เป็นค่าที่รับจาก request.POST
#         # ตัวอย่างเท่านี้จะขึ้นอยู่กับโครงสร้างของระบบฐานข้อมูลของคุณ
#     if request.method == "POST":  #updata profile
#         user = request.user
#         profile_image = request.FILES.get('profile_image')
#         if profile_image:
#             user.image = profile_image
#             user.save()
#         return redirect('/account')  # หลังจากอัปเดตข้อมูลเรียบร้อยแล้วให้ redirect ไปยังหน้า My account หรือหน้าที่คุณต้องการ
#     return render(request, 'settingprofile.html')  # หากเป็น GET request ให้แสดงแบบฟอร์มข้อมูลแก้ไขผู้ใช้


@login_required
def settingprofile(request):
    user = request.user  # Get the logged-in user
    user_age = calculate_age(user.date_of_birth)
    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'date_of_birth' : user.date_of_birth,
        'user_age': user_age,
    }
    # profile_image = request.FILES.get('profile_image')
    # if profile_image:
    #     user.image = profile_image
    #     user.save()
    #     # return redirect('/account')
    return render(request, 'Account/settingprofile.html', context)


@login_required
def changepassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            
            # ตรวจสอบว่ารหัสผ่านปัจจุบันถูกต้อง
            if request.user.check_password(current_password):
                # ตั้งรหัสผ่านใหม่และบันทึก
                request.user.set_password(new_password)
                request.user.save()
                
                # อัปเดตเซสชันและแจ้งให้ผู้ใช้รู้ว่ารหัสผ่านถูกเปลี่ยนแล้ว
                update_session_auth_hash(request, request.user)
                messages.success(request, 'รหัสผ่านถูกเปลี่ยนแล้ว')
            else:
                messages.error(request, 'รหัสผ่านปัจจุบันไม่ถูกต้อง')
        
        return render(request, 'Account/changepassword.html')
    else:
        template = loader.get_template('home.html')
        return HttpResponse(template.render())



from .models import Bannerslide
def home(request):
    slides = Bannerslide.objects.filter(active=True).order_by('order')

    if request.user.is_authenticated:
        template = loader.get_template('home.html')
        context = {
                    'username': request.user.username,
                    'slides': slides
                   }
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html', {'slides': slides})


def calender(request):
    template = loader.get_template('calender.html')
    return HttpResponse(template.render())

def moviereview(request):
    template = loader.get_template('moviereview.html')
    return HttpResponse(template.render())

