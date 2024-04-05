from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
import requests
from django.core.paginator import Paginator
import json

# Create your views here.

def index(request):

    return render(request,'app1/index.html')

    


