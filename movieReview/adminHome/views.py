from decimal import Decimal
import json
from django.db import transaction
from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.shortcuts import render
from django.views.decorators.cache import never_cache

# Create your views here.
# from .forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth import login, authenticate, logout

from star.models import *
from movies.models import *
from .forms import CommentForm, SignupForm
from datetime import date
from django.contrib.auth import update_session_auth_hash
# from django.shortcuts import render, redirect
# from .forms import SignupForm

from .models import *

#---------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from adminHome.models import Premium, Premium_list
#---------------------------------------------

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

def log_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    with open('ad.txt', 'a') as file:
        file.write(ip + '\n')


# from django.db.models import Q
from django.shortcuts import render
from django.template import RequestContext

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
import datetime


# Calendar scraper
def calendarscraper(request, year=None, month=None):
    if year is None or month is None:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
    else:
        year = int(year)
        month = int(month)

    url = f'https://www.boxofficemojo.com/calendar/{year}-{month}-01'
    current_year = datetime.datetime.now().year
    years = range(current_year + 2, 1923, -1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    all_tr_tags = soup.find_all('tr')
    all_list = []
    date = ""
    headdate = []
    for tr_tag in all_tr_tags:
        if tr_tag.get('class') and 'mojo-group-label' in tr_tag.get('class'):
            text = tr_tag.text.strip()
            date = text
            continue
        else:
            for m in tr_tag.find_all('td', {'class': 'a-text-left mojo-header-column mojo-truncate mojo-field-type-release mojo-cell-wide'}):
                moviename = m.find('div', {'class': 'a-section a-spacing-none mojo-schedule-release-details'})
                movietag = m.find('div', {'class': 'a-section a-spacing-none mojo-schedule-genres'})

                img_tag = m.find('img')
                if img_tag:
                    image = img_tag.get('src')
                else:
                    image = "No Image"

                if moviename:
                    name = moviename.find('a').text
                else:
                    name = "Don't have name"

                if movietag:
                    tag = movietag.text.replace('\n', '').replace('            ', ' ').replace('    ', '')
                else:
                    tag = "No Tag"

                with_divs = m.find_all('div', {'class': 'a-section a-spacing-none'})
                filtered_with_divs = [div for div in with_divs if div.find('span', {'class': 'a-text-bold'})]

                if filtered_with_divs:
                    actor = filtered_with_divs[0].text.replace('With:', '')
                else:
                    actor = "No Actor"

                # Append data to all_list with correct date
                all_list.append({
                    'image': image,
                    'name': name,
                    'tag': tag,
                    'actor': actor,
                    'date': date
                })
                if date not in headdate :
                    headdate.append(date)



    context = {
        'all_list': all_list,
        'headdate': headdate,
        'years':years,
        'year':year,
        'month':month,
        'url':url

    }
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    else:
        return render(request, 'calender.html', context)


#Calendar TH
def calendarTH(request):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    url = "https://www.majorcineplex.com/movie#movie-page-coming"
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text)
    calendarzone = soup.find('div',{'class':'box-movie-coming'})
    headdate_list=[]
    date = ''
    all_list = []
    for m1 in calendarzone.find_all('div', {'class': 'bma-movie-list'}):
        date = m1.find('div', {'class': 'bmaml-month'}).text
        headdate_list.append(date)
        for m2 in m1.find_all('div', {'class': 'ml-box'}):
            datezone = date
            
            name =m2.find('div', {'class': 'mlb-name'}).text.strip()
            release = m2.find('div', {'class': 'mlb-date'}).text.strip()
            
            # Tag
            tag = m2.find('span', {'class': 'genres_span'})
            tagl = tag.text.strip() if tag else "Don't have tag yet"
            
            # Time
            time = m2.find('div', {'class': 'mlbc-time'}).text.strip()
            timel = time if time != '00 ชม. 00 นาที' else "Don't know yet"
            
            # Image
            div_tag = m2.find('div', {'class': 'mlb-cover adv_tic'}) or m2.find('div', {'class': 'mlb-cover'})
            if div_tag:
                style_attribute = div_tag.get('style')
                if style_attribute:
                    url_start_index = style_attribute.find('url(') + len('url(')
                    url_end_index = style_attribute.find(')')
                    image_url = style_attribute[url_start_index:url_end_index].strip('"')
                    img = image_url
            all_list.append({
                'name':name,
                'datezone':datezone,
                'release':release,
                'tag':tagl,
                'time':timel,
                'image':img,
            })
    context = {
        'headdate': headdate_list,
        'all_list':all_list,
    }

    return render(request, 'calenderTH.html', context)

#Scarping Movie Comment
def moviecommentlink(moviename):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    moviename = str(moviename)
    search_url ='https://www.imdb.com/find?q='+moviename+'&s=tt&ttype=ft&ref_=fn_ft'
    print(search_url)
    data = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(data.text)
    linkmovie = soup.find('div',{'class':'sc-17bafbdb-2 iUyFfD'})
    link_element = linkmovie.find('a', {'class': 'ipc-metadata-list-summary-item__t'})
    linkcomment = ""
    link_element = linkmovie.find('a', {'class': 'ipc-metadata-list-summary-item__t'})
    if link_element:
        href_value = link_element.get('href')
        linkcomment = href_value.split('?')[0]
    else:
        print("Link element not found")
    url = 'https://www.imdb.com' + linkcomment + 'reviews?ref_=tt_urv'
    
    return url


# 404 page
def handler404(request, *args, **argv):
    response = render('404.html', {},
    context_instance=RequestContext(request))
    response.status_code = 404
    return response

# search.html 
def search(request):
    search_query = request.GET.get('q', '')  # รับค่าจากคิวรีพารามิเตอร์ 'q'
    # search_query = search.replace(" ", "") # ฟังก์ชั่นฟวย
    stars = []  # เริ่มต้นด้วยลิสต์ว่างสำหรับ stars
    movies =[]
    stars_images = [] # เริ่มต้นด้วยลิสต์ว่างสำหรับ star image 
    movies_images = []
    context = {}
    try:
        search_year = int(search_query)
        year_lookup = True
    except ValueError:
        year_lookup = False
    if search_query:  # ถ้ามีการค้นหาที่ส่งมา
        if search_query.startswith('#'):
            # ถ้า search_query เริ่มต้นด้วย # ให้ค้นหาชื่อประเภทหนัง
            idtage = MovieTag.objects.filter(name__icontains=search_query[1:]).values_list('id', flat=True).first()
        else:
            idtage = None
        if year_lookup:
            stars = Star.objects.filter(born_date__year=search_year)  # ค้นหาดาราที่เกิดในปีที่ค้นหา
        else:
            stars = Star.objects.filter(name__icontains=search_query)  # ค้นหาดาราที่มีชื่อตรงกับคำค้น !!(name_icontains = search ) ==== (sql) WHERE headline ILIKE '%ชื่อ%'; 
        
        for star in stars:
            # Get the main image for each star
            main_image = star.local_star_images.filter(mainstar=True, is_visible=True).first()
            if not main_image:
                main_image = star.url_star_images.filter(mainstar=True, is_visible=True).first()
            
            stars_images.append({
                'star': star,
                'main_image': main_image,
            })

        if year_lookup:
            movies = Movie.objects.filter(release_date__year=search_year)
        else:
            if idtage:
                # หาก search_query เป็นประเภทหนัง ให้ค้นหาตามประเภท
                movies = Movie.objects.filter(tags=idtage)
            
            else:
                # หาก search_query ไม่ใช่ปี ให้ค้นหาตามชื่อหนัง
                movies = Movie.objects.filter(name__icontains=search_query)
        
        for movie in movies:
            # ภาพหลักหรับหนังแต่ละเรื่อง
            main_local_image = movie.local_images_movie.filter(mainmovie=True, is_visible=True).first()
            
            # ภาพ URL หลักหรับหนังแต่ละเรื่อง
            main_url_image = movie.url_movie_images.filter(mainmovie=True, is_visible=True).first()

            # Determine which main image to use
            main_image = main_local_image or main_url_image

            movies_images.append({
                'movie': movie,
                'main_image': main_image,
            })

        context={
            'search_query':search_query,
            'star':stars,
            'stars_images': stars_images,
            'movie':movies,
            'movies_images':movies_images,

        }# context จะถูกส่งไปยัง template ทุกครั้ง แต่จะมี stars เฉพาะเมื่อมีการค้นหา
    return render(request, 'search.html', context)


@login_required
def update_user(request):
    user = request.user
    if request.method == 'POST':
        # รับข้อมูลจาก POST request
        new_firstname = request.POST.get('firstname')
        new_lastname = request.POST.get('lastname')
        new_email = request.POST.get('email')
        new_image = request.FILES.get('profile_image')
        # อัปเดตข้อมูลผู้ใช้ในฐานข้อมูล
        if new_email == user.email:
            # messages.error(request, 'There is already a user using this email.')]
            pass
        elif User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
            # messages.error(request, 'There is already a user using this email.')]
            print(User.objects.filter(email=new_email).exclude(pk=user.pk).exists())
            return JsonResponse({"message": "There is already a user using this email."})
        
        user.first_name = new_firstname
        user.last_name = new_lastname
        user.email = new_email
        # ถ้ามีรูปภาพเก่าในโมเดล, ลบมัน
        if new_image:
            if user.image and user.image.name != 'profile_images/istockphoto.jpg':
                user.image.delete(save=False)
            user.image = new_image
        user.save()
            # messages.success(request, 'ข้อมูลของคุณถูกอัปเดตแล้ว')
        return JsonResponse({"message": "Update Successfully."})
    return redirect('account')


@login_required
def get_user_data(request):
    try:
        user = request.user
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        return JsonResponse(user_data)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


from django.http import JsonResponse
from django.contrib.auth.models import User

def check_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email=email).exists()
    }
    return JsonResponse(data)


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
                user.image = 'profile_images/istockphoto.jpg' 
                user.save()
            login(request, user)
            return redirect('home')  # Redirect to a 'home' view, for instance.
    else:
        form = SignupForm()
    return render(request, 'Login_Register/register.html', {'form': form}) #form จะถูกหรือไม่ view จะส่งกลับ HttpResponse ในทุกสถานการณ์.

#Login
def login_view(request):
    log_user_ip(request)
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
            messages.error(request, 'Username or Email is incorrect.')
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


# logout
def logout_view(request):
    logout(request)
    return redirect('login')


def calculate_age(date_of_birth):
    if date_of_birth:
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        return age
    else:
        return 0 


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
            'user_age': user_age,
            'coin' : user.coin
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
        return redirect('account')
    return render(request, 'Account/changepassword.html')# กำหนดเส้นทางของ template ที่คุณใช้


from .models import Bannerslide

# หน้าหลัก
def home(request):
    log_user_ip(request)
    slides = Bannerslide.objects.filter(active=True).order_by('order')
    movies = Movie.objects.filter(is_show='1')
    movie_main_images = []

    for movie in movies:
        # ตรวจสอบและกำหนด main_image ในนี่
        main_local_image = LocalImage.objects.filter(movie_id=movie.id, mainmovie=True).first()
        if main_local_image:
            movie.main_image = main_local_image
        else:
            main_url_image = URLImage.objects.filter(movie_id=movie.id, mainmovie=True).first()
            movie.main_image = main_url_image
        
        # ตรวจสอบและกำหนด sentiment
        movie_sentiment = MovieSentiment.objects.filter(movie_id=movie.id).values('positive','negative').first()
        if movie_sentiment:
            # ถ้า movie_sentiment ไม่เป็น None, เก็บข้อมูล sentiment ไว้ใน object movie
            movie.positive = movie_sentiment.get('positive', 0)
            movie.negative = movie_sentiment.get('negative', 0)
        else:
            # ถ้า movie_sentiment เป็น None, กำหนดค่าเริ่มต้น
            movie.positive = 0
            movie.negative = 0
        #Score
        avg_score_result = Comment.objects.filter(movie_id=movie.id).aggregate(average_score=Avg('score'))
        avg_score = avg_score_result.get('average_score',0)
        if avg_score:
            avg_score = round(avg_score, 1)
            movie.avg_score = avg_score
        else:
            avg_score = 0
            movie.avg_score = avg_score

    #New Movie
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    url = "https://www.rottentomatoes.com/browse/movies_in_theaters/sort:newest"
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text)
    imgmovie = []
    namemovie = []
    releasedate = []
    for c in soup.find_all('div',{'class':'flex-container'}):

        imgmovie.append(c.find('rt-img',{'class':'posterImage'}).get('src'))
        namemovie.append(c.find('span',{'class':'p--small'}).text.replace('\n        ','').replace('  ',''))
        releasedate.append(c.find('span',{'class':'smaller'}).text.replace('\n        ','').replace('  ','').replace('Opened ',''))
        if(len(imgmovie)==10):
            break
    NewMovie_list = zip(imgmovie,namemovie,releasedate)

    context = {
                'username': request.user.username,
                'slides': slides,
                'movies':movies,
                'mainmovie_image':movie_main_images,
                'newMovie':NewMovie_list
              }
    return render(request, 'home.html', context)

#coin shop - ร้านค้าเหรียญ
def coinshop(request):
    premiums = Premium.objects.all()
    user = request.user

    if request.method == 'GET':
        return render(request, 'coinshop.html', {'premiums': premiums})

    if request.method == 'POST' and request.user.is_authenticated:
        premium_id = request.POST.get('premium_id')

        try:
            premium_item = Premium.objects.get(pk=premium_id)
        except Premium.DoesNotExist:
            messages.error(request, "The selected product does not exist.")
            return redirect('coinshop')
    else:
        messages.error(request, "Please login to purchase products.")
        return redirect('login')    
    with transaction.atomic():  #Transaction Handling
        if premium_item.expires < date.today():
            messages.error(request, "Sorry. this product offer has expired.")
            return redirect('coinshop')

        elif premium_item.num <= 0:
            messages.error(request, "Sorry. this product is out of stock.")
            return redirect('coinshop')

        if request.user.coin >= premium_item.price:
            request.user.coin -= premium_item.price
            request.user.save()

            premium_item.num -= 1
            premium_item.save()

            # Record the purchase
            Premium_list.objects.create(user=request.user, premium=premium_item)
            subject = 'ขอบคุณที่ทำการซื้อสินค้าที่เรา'
            message = f'สวัสดีคุณ {user.username},\n\n'\
                    f'ขอบคุณที่ทำการซื้อสินค้า\n'\
                    'รายการสินค้า\n'\
                    f'"{premium_item.name}" ในราคา {premium_item.price} coins.\n'\
                    'หากมีข้อสงสัยหรือปัญหาเกี่ยวกับสินค้า กรุณาติดต่อเราได้ที่ Blueeye.or@gmail.com\n\n'\
                    'ด้วยความนับถือ,\n'\
                    'ทีมงาน MovieReview'
            from_email = 'your-email@gmail.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, "Purchase successful!")
        else:
            messages.error(request, "Not enough coins!")

    context = {
        'premiums': premiums
    }
    if request.user.is_authenticated:
        context.update({
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'coin': request.user.coin,
        })

    return render(request, 'coinshop.html', context)

#==========================================================================================
from langdetect import detect
def detect_language(text):
    try:
        # Detect the language of the text
        language = detect(text)
        return language
    except Exception as e:
        # Handle any exception (e.g., text is too short)
        return f"Error detecting language: {str(e)}"

# การประมวลผลข้อความ
import re
def preprocess(text):
    from nltk.corpus import stopwords
    stopwords_custom = ['oh', 'wow']
    # Remove special characters and convert to lowercase
    text = re.sub(r'\W', ' ', text.lower())
    # Remove unwanted words
    text = ' '.join([word for word in text.split() if word not in stopwords.words('english') and word not in stopwords_custom])
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

import joblib
def sentiment(text):
    #TODO ถ้าข้อความสั้นเกินไปจะ Detect ไม่เจอภาษา
    if detect_language(text) != 'en' and len(text) > 200:
        return "Neutral"
    else:
        # โหลดโมเดลและ CountVectorizer ที่ถูกฟิตแล้ว
        model = joblib.load('E:/Project_MovieReview707/movieReview/adminHome/ai/NueralNetwork_model.joblib')
        tfidf_v = joblib.load('E:/Project_MovieReview707/movieReview/adminHome/ai/tfidf_vectorizer.joblib')  # ต้องมีการบันทึก CountVectorizer ที่ถูกฟิตแล้วเป็นไฟล์
        
        # ปรับแต่งและแปลงข้อความเป็นเวกเตอร์
        processed_text = preprocess(text)
        text_vector = tfidf_v.transform([processed_text])
        
        # ทำนายและรีเทิร์นผลลัพธ์
        # return model.predict(text_vector)[0]
        prediction = model.predict(text_vector)
        return "Positive" if prediction[0] == 0 else "Negative"
#==========================================================================================

def movieSentiment(id):
    movie = get_object_or_404(Movie, pk=id)
    # check = MovieSentiment.objects.filter(movie=movie).exists()

    # คำนวณจำนวนความคิดเห็น Positive และ Negative (ไม่รวม Neutral)
    total_count = Comment.objects.filter(movie=movie).exclude(sentiment='Neutral').count()

    # คำนวณจำนวนความคิดเห็น Positive และ Negative แยกกัน
    positive_comments = Comment.objects.filter(movie=movie, sentiment='Positive').count()
    negative_comments = Comment.objects.filter(movie=movie, sentiment='Negative').count()

    # คำนวณเปอร์เซ็นต์
    positive_percent = (positive_comments / total_count) * 100 if total_count > 0 else 0
    negative_percent = (negative_comments / total_count) * 100 if total_count > 0 else 0

    sentiment, created = MovieSentiment.objects.update_or_create(
        movie=movie,
        defaults={'positive': positive_percent, 'negative': negative_percent}
    )


def filter_comment(queryset):
    with open('adminHome/ai/bad-words.txt', 'r') as file:
        bad_words = [word.strip() for word in file.readlines()]

    for comment in queryset:
        filtered_text = comment.data
        for word in bad_words:
            filtered_text = filtered_text.replace(word, '*' * len(word))
        comment.filtered_data = filtered_text  # สร้าง attribute ใหม่ไม่ได้บันทึกลงฐานข้อมูล

    return queryset

from django.db.models import Avg
from django.db.models import Count

# Movie review page
def moviereview(request, id):
    movie = get_object_or_404(Movie, pk=id)
    form = CommentForm(request.POST)  # Instantiate the form for POST; None will make it unbound for GET
    user = request.user # User
    directors = movie.director.all()
    writers = movie.writer.all()
    top_stars = MovieDetail.objects.filter(movie=movie, is_top=True)
    #######################################################
    #Scraping Movie Point
    # pointIMDB = moviepointscraping(str(movie.name))
    
    # linkscrapingcomment = moviecommentlink(movie.name)
    # urls=linkscrapingcomment
    # headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    # data = requests.get(urls, headers=headers)
    # soup = BeautifulSoup(data.text)
    # pointcomment = []
    # headcomment=[]
    # detailcomment = []
    # spoilcomment = []
    # for idx, m in enumerate(soup.find_all('div',{'class':'review-container'})):
    #     if idx >= 10:
    #         break
    #     rating_container = m.find('span', {'class': 'rating-other-user-rating'})
    #     if rating_container is not None:
    #         point = rating_container.find('span').text
    #         print(point)
    #         pointcomment.append(point)
    #     else:
    #         point = "Don't give point."
    #         print(point)
    #         pointcomment.append(point)
    #     headcomment.append(m.find('a',{'class':'title'}).text.replace('\n',''))
    #     detailcomment.append(m.find('div',{'class':'text show-more__control'}).text)
    #     spoil = m.find('span',{'class':'spoiler-warning'})
    #     if spoil is not None:
    #         spoilcomment.append(spoil.text)
    #     else:
    #         spoil = "Normal"
    #         spoilcomment.append(spoil)


    
    # all_list = zip(pointcomment,headcomment,spoilcomment,detailcomment)
    # moviecommentformIMDB()
    #######################################################
    #Star Image
    top_star_images = []  # ใช้ list เพื่อเก็บ URL ของรูปภาพ
    for star_detail in top_stars:
        star = star_detail.star  # ดึง object ของ Star

        # ตรวจสอบ LocalImage ที่เป็น mainstar
        local_images = LocalImage.objects.filter(star=star, mainstar=True)
        
        if local_images.exists():
            # ถ้ามี LocalImage
            image_url = local_images.first().image.url
        else:
            # ถ้าไม่มี LocalImage, ใช้ URLImage
            url_images = URLImage.objects.filter(star=star, mainstar=True)
            if url_images.exists():
                # ถ้ามี URLImage
                image_url = url_images.first().image_url
            else:
                # ถ้าไม่มีทั้ง LocalImage และ URLImage
                image_url = None
        top_star_images.append(image_url)
    #######################################################
    #User comment
    if user.is_authenticated :  # Check if the user
        commented = Comment.objects.filter(movie=movie, user=user).first()  
        other_comments = Comment.objects.filter(movie=movie).exclude(user=user)
        other_top = Comment.objects.filter(movie=movie).exclude(user=user).annotate(likes_count=Count('like')).order_by('-likes_count')
    else:
        commented = None
        other_comments = Comment.objects.filter(movie=movie).exclude()
        other_top = Comment.objects.filter(movie=movie).annotate(likes_count=Count('like')).order_by('-likes_count') 
    #Top coment
    # Fetch the top comment based on likes
    # Assuming you want to exclude the current user's comment from being the top comment
    top_comment = other_top.first() if other_comments else None
    # คำนวณคะแนนเฉลี่ยของความคิดเห็น
    avg_score_result = Comment.objects.filter(movie=movie).aggregate(average_score=Avg('score'))
    avg_score = avg_score_result.get('average_score',0)
    #######################################################
    #Score
    if avg_score is not None:
        avg_score = round(avg_score, 1)
    else:
        avg_score = 0
    #######################################################

    if request.method == 'POST':
        if commented:  # ตรวจสอบว่าผู้ใช้แสดงความคิดเห็นแล้วหรือไม่
            form = CommentForm(request.POST, instance=commented)  # ใช้ CommentForm ผูกกับความคิดเห็นที่มีอยู่แล้ว
        else:
            form = CommentForm(request.POST)     #ไม่มีความคิดเห็นที่มีอยู่ สร้างความคิดเห็นใหม่ 
        if form.is_valid():
            print(form)
            comment = form.save(commit=False)
            comment.spoiler = True if request.POST.get('spoiler') == '1' else False
            # print(comment.spoiler)
            comment.sentiment = sentiment(comment.data)
            comment.user = request.user
            comment.movie = movie
            comment.save()
            movieSentiment(id)
            return redirect('moviereview', id=id)

    if request.method == 'GET':
        try:
            video = get_object_or_404(Video, movie=movie)
        except:
            video = None
        
        # Images main movie
        mainmovie_image = None
        local_mainmovie_image = LocalImage.objects.filter(is_visible=True, mainmovie=True, movie=movie)
        url_mainmovie_image = URLImage.objects.filter(is_visible=True, mainmovie=True, movie=movie)

        if local_mainmovie_image.exists():
            mainmovie_image = local_mainmovie_image.first()
        elif url_mainmovie_image.exists():
            mainmovie_image = url_mainmovie_image.first()

        # Image movie
        local_images = LocalImage.objects.filter(is_visible=True, movie=movie, mainmovie=0)
        url_images = URLImage.objects.filter(is_visible=True, movie=movie, mainmovie=0)
        movie_images = list(local_images) + list(url_images)

        # get MovieSentiment
        movie_sentiment = MovieSentiment.objects.filter(movie=movie)

        # like comment
        if user.is_authenticated:
            # Check if the user has already liked the comment
            is_liked = Like.objects.filter(user=user, comment=commented).exists()
            # Get all comments liked by the user
            # liked_comments = Comment.objects.filter(like__user_id=user.id).distinct()
            # liked_comments = [{'id': comment.id} for comment in liked_comments]
            # print(liked_comments)
            liked_commentsss = Comment.objects.filter(like__user=request.user).values_list('id', flat=True)
            liked_commentsss = [comment for comment in liked_commentsss]
        else:
            is_liked = False
            liked_commentsss = None
        # คำนวณจำนวนความคิดเห็น Positive และ Negative (ไม่รวม Neutral)
        if movie_sentiment.exists():
            positive = round(movie_sentiment[0].positive)
            negative = round(movie_sentiment[0].negative)
        else:
            positive = 0
            negative = 0

        other_comments = other_comments.annotate(likes_count=Count('like'))
        combined_data = zip(top_star_images, top_stars)
        # filter comment
        if top_comment:
            other_comments = other_comments.exclude(id=top_comment.id)
            top_comment = filter_comment([top_comment])
            top_comment = top_comment[0] if top_comment else None
        else:
            top_comment = None
        if commented == None:
            other_comments = filter_comment(list(other_comments))
        else: 
           commented = filter_comment([commented])
           other_comments = filter_comment(list(other_comments))
        commented = commented[0] if commented else None
        print(top_comment)
        context = {
            'combined_data': combined_data,
            'movie': movie,
            'user': user,
            'scoreAvg':avg_score,
            'directors':directors,
            'writers':writers,
            'topcast': top_stars,
            'star_images':top_star_images,
            'mainmovie_image': mainmovie_image,
            'movie_image': movie_images,
            'video': video,
            'form': form,
            'commented':commented,
            'other_comments':other_comments,
            'top_comment':top_comment,
            'is_liked': is_liked,
            'liked_comments':liked_commentsss,
            'positive': positive,
            'negative': negative,
        }
        return render(request, 'moviereview.html', context)
    return render(request, 'moviereview.html', context)

#Scraping Movie Data
def scrape_movie_data(request, movie):
    movie_name = movie
    print(movie_name)
    if movie_name:
        linkscrapingcomment = moviecommentlink(movie_name)
        urls = linkscrapingcomment
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        data = requests.get(urls, headers=headers)
        soup = BeautifulSoup(data.text)
        
        pointcomment = []
        headcomment = []
        detailcomment = []
        spoilcomment = []
        
        for idx, m in enumerate(soup.find_all('div',{'class':'review-container'})):
            if idx >= 10:
                break
            rating_container = m.find('span', {'class': 'rating-other-user-rating'})
            if rating_container is not None:
                point = rating_container.find('span').text
                pointcomment.append(point)
            else:
                point = "Don't give point."
                pointcomment.append(point)
            headcomment.append(m.find('a',{'class':'title'}).text.replace('\n',''))
            detailcomment.append(m.find('div',{'class':'text show-more__control'}).text)
            spoil = m.find('span',{'class':'spoiler-warning'})
            if spoil is not None:
                spoilcomment.append(spoil.text)
            else:
                spoil = "Normal"
                spoilcomment.append(spoil)
        all_list = zip(pointcomment, headcomment, spoilcomment, detailcomment)
        context = {
            'all_list': [dict(zip(['point', 'head', 'spoil', 'detail'], item)) for item in all_list],
        }
        return JsonResponse(context)
    else:
        # หากไม่ได้รับ id หรือชื่อของภาพยนตร์
        return JsonResponse({'error': 'Missing movie id or name'}, status=400)

from django.http import JsonResponse
from .models import Comment, Like  
from django.db.models import F

def like_comment(request, comment_id):
    user = request.user
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment does not exist'}, status=404)

    # Check if the user has already liked the comment
    if user:
        is_liked = Like.objects.filter(user=user, comment=comment).exists()
        print(is_liked)
    # Get all comments liked by the user    
    liked_comments = Comment.objects.filter(like__user_id=user.id).distinct()
    liked_comments = [{'id': comment.id} for comment in liked_comments]
    
    if request.method == 'POST':
        if is_liked:
            # User already liked, so unlike it
            Like.objects.filter(user=user, comment=comment).delete()
            comment.toplike = F('toplike') - 1
            comment.save()
            is_liked = False
        else:
            # User has not liked it yet, so create a like
            Like.objects.create(user=user, comment=comment)
            comment.toplike = F('toplike') + 1
            comment.save()
            is_liked = True
        comment.refresh_from_db()
        likes_count = Like.objects.filter(comment_id=comment.id).count()
    print(comment.toplike)
    context = {
        'is_liked': is_liked,
        'comment_id': comment_id,
        'liked_comments':liked_comments,
        'likes_count':likes_count,
        'toplike': comment.toplike,
    }
    return JsonResponse(context)



def report_comment(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Please log in to report a comment.'}, status=401)

    try:
        comment = Comment.objects.get(id=comment_id)
        data = json.loads(request.body.decode('utf-8'))
        if data.get('issueType') == 'other':
            reason = data.get('customText')
        else:
            reason = data.get('issueType')

        # Create a new Report instance and save
        Report.objects.create(comment=comment, reason=reason)

        return JsonResponse({'message': 'Report submitted successfully.'}, status=201)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def actor(request, id):
    # search_query = request.GET.get('search', None)
    # star = Star.objects.filter(name__icontains=search_query) # ฟังชัน icontains สตริง โดยไม่คำนึงถึงตัวพิมพ์เล็กและตัวพิมพ์ใหญ่
    star = get_object_or_404(Star, pk=id)
    startype = [job.name for job in star.job.all()]
    height  = '{:.1f}'.format(star.height * 3.28084)
    official_list = star.official_sites_set.all()
    alternative_names = AlternativeNames.objects.filter(star=star)
    relatives = Relatives.objects.filter(star=star)
    other_works = OtherWorks.objects.filter(star=star)
    # Born
    born_date = star.born_date
    born_location = star.born_location
    # Died
    died_date = star.died_date
    died_location = star.died_location
    # Spouse
    spouse = Spouses.objects.filter(star=star)
    # spouse_to_others = star.spouse_star.all()
    # Children
    children_of_star = Children.objects.filter(star=star)
    children = [child.child_name for child in children_of_star if child.child_name is not None]
    # Parent
    parent_relations = Children.objects.filter(child_name=star)
    parent_names = [relation.star.name for relation in parent_relations]

    # ดึงรูปภาพจาก LocalImage และ URLImage ที่เป็น mainstar สำหรับ star นี้
    mainstar_image = None
    local_mainstar_image = LocalImage.objects.filter(is_visible=True, mainstar=True, star=star)
    url_mainstar_image = URLImage.objects.filter(is_visible=True, mainstar=True, star=star)

    if local_mainstar_image.exists():
        mainstar_image = local_mainstar_image.first()
    elif url_mainstar_image.exists():
        mainstar_image = url_mainstar_image.first()
    # Image
    local_images = LocalImage.objects.filter(is_visible=True, star=star, mainstar=0)
    url_images = URLImage.objects.filter(is_visible=True, star=star, mainstar=0)

    # You may want to combine them into one list if they are treated similarly in the template
    non_mainstar_images = list(local_images) + list(url_images)
    
    context = {
        'star': star,
        'jobs_list': startype,
        'height':height,
        'official_list':official_list,
        'mainstar_image':mainstar_image,
        'alternative_names':alternative_names,
        'relatives':relatives,
        'other_works':other_works,
        'born_date':born_date,
        'born_location':born_location,
        'died_date':died_date,
        'died_location':died_location,
        'spouse':spouse,
        # 'spouse_to_others':spouse_to_others,
        'children':children,
        'parent':parent_names,
        'non_mainstar_images':non_mainstar_images,
    }
    return render(request, 'actor.html',context)


from django.conf import settings
from django.shortcuts import redirect

# 404 page 
def error_404_view(request, exception):
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_view(request):
    
    context = {
    }
    
    return render(request, 'admin/dashboard.html', context)

# ========================================================================================================================
# minigame
def minigame(request):
    category = request.GET.get('category')
    print(category)
    if not request.user.is_authenticated:
        return redirect('login')
        
    if category == 'Movie':
        movies = list(Movie.objects.order_by('?')[:4])
        mainmovie_images = []
        answer = movies[0].name
        for movie in movies:
            main_local_image = LocalImage.objects.filter(movie=movie, mainmovie=True).first()
            if main_local_image:
                mainmovie_images.append(main_local_image.image.url)
            else:
                main_url_image = URLImage.objects.filter(movie=movie, mainmovie=True).first()
                if main_url_image:
                    mainmovie_images.append(main_url_image.image_url)
                else:
                    mainmovie_images.append(None) # หรือ URL รูปภาพเริ่มต้น
        mainmovie_image = mainmovie_images[0]
        movie_names = [movie.name for movie in movies]
        random.shuffle(movie_names)
        context = {
            'mainmovie_images': mainmovie_image,
            'answer': answer,
            'main_names': movie_names,
        }
        print(context)
    elif category == 'Star':
        local_main_image = LocalImage.objects.filter(is_visible=True, mainstar=True).order_by('?').first()
        url_main_image = URLImage.objects.filter(is_visible=True, mainstar=True).order_by('?').first()
        main_images = local_main_image, url_main_image
        main_images = [img for img in main_images if img]  # Filter out None values
        random.shuffle(main_images)

        if not main_images:  # If no images are found
            return HttpResponse("No images found", status=404)  # Handle this case appropriately

        main_image = main_images[0]  # Now we are sure it's not None
        print(main_image)
        main_star_name =  [str(star.name) for star in main_image.star.all()]
        
        # remove list
        delimiter = ", "
        main_star_name = delimiter.join(main_star_name)

        # Prepare star names
        star_names = [main_star_name] + [star.name for star in Star.objects.exclude(name=main_star_name).order_by('?')[:3]]
        random.shuffle(star_names)
        print(main_star_name)
        context = {
            'mainstar_image': main_image.image.url if isinstance(main_image, LocalImage) else main_image.image_url,
            'answer': main_star_name,
            'main_names': star_names,
        }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print(context)
        return JsonResponse(context) 
    else:
        return render(request, 'minigame.html')

@login_required
@require_POST    
def updatecoin(request):
    user = request.user
    user.coin += Decimal('0.20')
    user.save()
    return JsonResponse({"status": "success"}) 

@login_required
def update_session(request):
    user = request.user
    
    # Attempt to retrieve the user's gameplay record, assuming it's reset daily
    gameplay, created = GamePlay.objects.get_or_create(user=user)
    
    if gameplay.sessions_today >= 3:
        # User has reached the limit for the day
        return JsonResponse({'error': 'You have reached the daily game limit.'}, status=403)
    
    # Increment the session count and save
    gameplay.sessions_today += 1
    gameplay.save()
    
    # Successfully updated the session count
    return JsonResponse({'message': 'Session updated successfully'})
# ========================================================================================================================
# หน้าเกี่ยวกับเรา
def about_us(request):
    return render(request, 'Login_Register/about_us.html')

# ========================================================================================================================
# ใช้เพื่อทดสอบ
def test(request):
    # request_type = request.GET.get('type')

    # if request_type == 'get_movies':
    #     movies = Movie.objects.filter(is_show=True).values('id', 'name')
    #     return JsonResponse(list(movies), safe=False)

    # elif request_type == 'get_user_login_count':
    #     user_login_count = 10  # Replace with your actual logic to get the count
    #     return JsonResponse({'count': user_login_count})

    # elif request_type == 'get_comments_data':
    #     movie_id = request.GET.get('movie_id')
    #     comments = Comment.objects.filter(movie_id=movie_id).values('sentiment').annotate(count=Count('sentiment'))
    #     data = {sentiment['sentiment']: sentiment['count'] for sentiment in comments}
    #     return JsonResponse(data)

    # elif request_type == 'get_movie_sentiments':
    #     movie_id = request.GET.get('movie_id')
    #     sentiment_data = MovieSentiment.objects.filter(movie_id=movie_id).values('positive', 'negative')
    #     if sentiment_data:
    #         return JsonResponse(sentiment_data[0])
    #     return JsonResponse({'positive': 0, 'negative': 0})

    # return JsonResponse({'error': 'Invalid request type'}, status=400)
    return render(request, 'test.html')
# ========================================================================================================================
#admin custom view
# my_custom_view
    # views.py

# def dashboard_view(request):
#     # สมมติว่าคุณเก็บข้อมูลกราฟใน database
#     data = {
#         'labels': ["January", "February", "March", "April", "May", "June", "July"],
#         'datasets': [{
#             'label': "Data",
#             'backgroundColor': "rgba(255, 99, 132, 0.2)",
#             'borderColor': "rgba(255, 99, 132, 1)",
#             'borderWidth': 1,
#             'data': [10, 20, 30, 40, 50, 60, 70]
#         }]
#     }
#     # return JsonResponse(data)
#     return render(request, 'admin/dashboard.html', {'data': data})