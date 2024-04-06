from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
import requests
from requests import Session
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
import requests_cache
from .getcoinlist import getcoinlist


# Create your views here.

def index(request):

    return render(request,'app1/index.html')


def generatecoins(request):

    data = getcoinlist()

    return JsonResponse({
        "data": data['data']
    }, status=200)




