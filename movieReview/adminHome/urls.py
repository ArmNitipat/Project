from django.urls import path
from adminHome import views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    path('calender/',views.calender),
    path('login/',views.login_view, name='login'),
    path('register/',views.signup_view, name='register'),
    path('account/',views.account, name='account'),
    path('settingprofile/',views.settingprofile, name='settingprofile'),
    path('update_user/', views.update_user, name='update_user'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('resetpassword2/', views.resetpassword2, name='resetpassword2'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)