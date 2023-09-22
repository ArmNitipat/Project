from django.urls import path
from adminHome import views
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.home),
    path('calender',views.calender),
    path('login/',views.login),
    path('register',views.register, name='register'),
    path('signup',views.signup, name='signup'),
]

# urlpatterns = [
#     path('login/', auth_views.LoginView.as_view(), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
# ]