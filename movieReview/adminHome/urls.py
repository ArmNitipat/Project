from django.urls import path
from adminHome import views
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('index',views.index),
    path('dataMG',views.dataMG),
    path('reportCM',views.reportCM),
    path('dashBD',views.dashBD),
    path('',views.home),
    path('calender',views.calender),
    path('login',views.login),
    path('register',views.register), 
]
