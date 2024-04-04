from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request,'app1/index.html')


def registerpage(request):
    context = {}
    return render(request,'app1/register.html',context)

def loginpage(request):
    context = {}
    return render(request,'app1/login.html',context)


