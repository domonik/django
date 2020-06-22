from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from accounts import views



urlpatterns = [
    url('login', views.loginPage, name="login"),
    url('register', views.registerPage, name="register"),
    url('logout', views.logoutUser, name="logout")
    
]
