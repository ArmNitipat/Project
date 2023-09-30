from django.urls import path
from adminHome import views
from . import views

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

]