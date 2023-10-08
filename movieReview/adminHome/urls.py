from django.urls import path #,re_path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

#------------------------------------------------------------------------------------
# from .views import send_my_email
from django.contrib.auth import views as auth_views
#------------------------------------------------------------------------------------

urlpatterns = [
    path('',views.home, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('calender/',views.calender),
    path('login/',views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/',views.signup_view, name='register'),
    path('account/',views.account, name='account'),
    path('settingprofile/',views.settingprofile, name='settingprofile'),
    path('update_user/', views.update_user, name='update_user'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('credentials/', views.check_credentials, name='credentials'),
    path('resetpassword/', views.reset_password, name='resetpassword'),
    path('moviereview/', views.moviereview, name='moviereview'),
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------
    # path('send_my_email/', send_my_email, name='send_my_email'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
    # re_path(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # -----------------------------------------------------------------------------------------------------------------------------------------------------------
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


