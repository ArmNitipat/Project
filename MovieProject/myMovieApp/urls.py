from django.urls import path
from myMovieApp import views
urlpatterns = [
    path('',views.index),
    path('calender',views.calender),
    path('login',views.login)
]