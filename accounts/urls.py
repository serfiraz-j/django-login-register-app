from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('index', views.login),
    path('login', views.login),
    path('register', views.register, name="register"),
    path('change_password', views.change_password, name="change_password"),
    path('logout', views.logout, name="logout"),
    path('welcome', views.welcome, name="welcome")

]
