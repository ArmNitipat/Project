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
            if user.image and user.image.name != 'profile_images/istockphoto612x612.jpg':
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
            send_mail(
                'Movie Review การสมัครสมาชิก',
                f'เรายินดีที่ คุณ {user.username} ได้มาเป็นสมาชิกกับเรา',
                'your-email@gmail.com',
                [user.email],  # Add recipient list here
                fail_silently=False,
            )
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
            context['login_error'] = "This username and password could not be found."
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

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
import random
#เตรียมลบ
# def check_credentials(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#       # return redirect('resetpassword')

#     return render(request, 'Login_Register/credentials.html')
from django.core.exceptions import MultipleObjectsReturned

def check_credentials(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')

        try:
            user = User.objects.get(username=username, email=email)

            # Generate OTP
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            
            # Send OTP via email
            send_mail(
                'รหัส OTP สำหรับการรีเซ็ตรหัสผ่าน',
                f'รหัส OTP ของคุณคือ: {otp}',
                'your-email@gmail.com',
                [email],
                fail_silently=False,
            )
            request.session['user_id_for_reset'] = user.id
            request.session['reset_email'] = email
            return redirect('verify_otp')
        
        except User.DoesNotExist:
            messages.error(request, 'ไม่พบชื่อผู้ใช้หรืออีเมล์ในระบบ')
            return redirect('credentials')
        
        except MultipleObjectsReturned:
            # This handles the rare case where two user objects have the same email and username
            messages.error(request, 'พบปัญหาในระบบ, กรุณาติดต่อผู้ดูแล')
            return redirect('credentials')

    return render(request, 'Login_Register/credentials.html')


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        # ดึง OTP จาก session ที่เราเซ็ตไว้ตอนส่งรหัสไปยังผู้ใช้
        actual_otp = request.session.get('otp')
        
        # ตรวจสอบว่า OTP ที่ผู้ใช้ป้อนเข้ามาตรงกับ OTP ใน session หรือไม่
        if entered_otp == str(actual_otp):
            # ถ้าตรง, OTP ถูกต้อง ทำกระบวนการอื่นๆต่อ
            del request.session['reset_email']
            return redirect('resetpassword')
        else:
            # ถ้าไม่ตรง, OTP ไม่ถูกต้อง
            messages.error(request, 'Incorrect OTP')
            return redirect('verify_otp')
    return render(request, 'Login_Register/verify_otp.html')


# from django.http import HttpResponse
# from django.core.mail import send_mail

# def send_email_view(request):
#     try:
#         send_mail(
#             'Subject here',
#             'Here is the message.',
#             'from@example.com',
#             ['to@example.com'],
#             fail_silently=False,
#         )
#         return HttpResponse("Email sent successfully!")
#     except Exception as e:
#         return HttpResponse(f"Error: {str(e)}")


from django.contrib.auth.forms import SetPasswordForm
def reset_password(request):
    user_id = request.session.get('user_id_for_reset')
    if user_id is not None:
        user = User.objects.get(id=user_id)
        
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                del request.session['user_id_for_reset']
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


# @login_required
# def settingprofile(request):
#     user = request.user  # Get the logged-in user
#     user_age = calculate_age(user.date_of_birth)
#     context = {
#         'username': user.username,
#         'first_name': user.first_name,
#         'last_name': user.last_name,
#         'email': user.email,
#         'date_of_birth' : user.date_of_birth,
#         'user_age': user_age,
#     }
#     return render(request, 'Account/settingprofile.html', context)
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

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'date_of_birth' : user.date_of_birth.strftime('%d-%m-%Y'),
            'user_age': user_age,
        }
        return JsonResponse(data)
    else:
        return render(request, 'Account/settingprofile.html', context)


# @login_required
# def changepassword(request):
    # if request.user.is_authenticated:
    #     if request.method == 'POST':
    #         current_password = request.POST.get('current_password')
    #         new_password = request.POST.get('new_password')
            
    #         # ตรวจสอบว่ารหัสผ่านปัจจุบันถูกต้อง
    #         if request.user.check_password(current_password):
    #             # ตั้งรหัสผ่านใหม่และบันทึก
    #             request.user.set_password(new_password)
    #             request.user.save()
                
    #             # อัปเดตเซสชันและแจ้งให้ผู้ใช้รู้ว่ารหัสผ่านถูกเปลี่ยนแล้ว
    #             update_session_auth_hash(request, request.user)
    #             # messages.success(request, 'รหัสผ่านถูกเปลี่ยนแล้ว')
    #             return render(request, 'Account/account.html')
    #         # else:
    #             # messages.error(request, 'รหัสผ่านปัจจุบันไม่ถูกต้อง')
    #     return render(request, 'Account/changepassword.html')
    # else:
    #     template = loader.get_template('home.html')
    #     return HttpResponse(template.render())

@login_required
def changepassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password1')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = request.user
        if not user.check_password(old_password):
            messages.error(request, 'รหัสผ่านเก่าไม่ถูกต้อง')
            return redirect('changepassword')

        if new_password1 != new_password2:
            messages.error(request, 'รหัสผ่านใหม่และการยืนยันรหัสผ่านไม่ตรงกัน')
            return redirect('changepassword')

        user.set_password(new_password1)
        user.save()
        # Update session hash to keep the user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, 'เปลี่ยนรหัสผ่านเรียบร้อยแล้ว')
        return redirect('account')  # ปรับเปลี่ยนตามต้องการ
    return render(request, 'Account/changepassword.html')# กำหนดเส้นทางของ template ที่คุณใช้


from .models import Bannerslide
# Home page
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

def actor(request):
    template = loader.get_template('actor.html')
    return HttpResponse(template.render())

from django.conf import settings
from django.shortcuts import redirect

# 404 page 
def error_404_view(request, exception):
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')