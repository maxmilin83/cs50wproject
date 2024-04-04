from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/',views.registerpage,name="register"),
    path('login/',views.loginpage,name="login"),

]