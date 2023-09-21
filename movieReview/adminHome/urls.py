from django.urls import path
from adminHome import views
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.home),
    path('calender',views.calender),
    path('login',views.login),
    path('register',views.register, name='register'),
    path('signup',views.signup, name='signup'),
]
