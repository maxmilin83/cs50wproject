from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
from .coinsapi import getcoinlist,getcoin,gettrendingcoins,getcoinchart
from django.contrib import messages
from datetime import datetime
from users.models import CustomUser
from .models import Order
from django.contrib.auth import get_user_model
# Create your views here.

def index(request):

    return render(request,'app1/index.html')

def viewtrending(request):

    return render(request,'app1/trending.html')


def generatetrending(request):
    response = gettrendingcoins()

    if response['success']:
        
        return JsonResponse({
            "data": response['data']
        })
    else:
        messages.error(request,"Error fetching data")
        return JsonResponse({
            "error": response['error']},
            status=502
        )
    
def generatecoins(request):
    response = getcoinlist()
    
    if response['success']:
        
        return JsonResponse({
            "data": response['data']
        })
    else:
        messages.error(request,"Error fetching data")
        return JsonResponse({
            "error": response['error']},
            status=502
        )
    
def generatechart(request,coin,days):
    response = getcoinchart(coin,days)
    if response['success']:
        
        return JsonResponse({
            "data": response['data']
        })
    else:
        messages.error(request,"Error fetching data")
        return JsonResponse({
            "error": response['error']},
            status=502
        )

def viewcoin(request,coin):
    if request.user.is_authenticated:
        
        if request.method =="POST":
            print("test")
            
        allOrders = Order.objects.filter(user=request.user,coin=coin)


    try:
        response = getcoin(coin)
        if response['success']:
            response = response['data'][0]
            date = response['last_updated']
            dt = datetime.fromisoformat(date.rstrip("Z"))
            date = dt.strftime("%B %d, %Y, %I:%M %p")

            context = {"coin":response,
                        "date":date,
                        }
            if request.user.is_authenticated:
                context['orders']=allOrders
                
            return render(request,'app1/viewcoin.html',context)
        else:
            messages.error(request,"Error fetching coin data")
            return(redirect("index"))
    except IndexError:
            messages.error(request,"Error fetching coin data")
            return(redirect("index"))

    
    
def viewfunds(request):
    return render(request,"app1/funds.html")


def addfunds(request):
    if request.method =="POST":

        currentuserobject = get_user_model().objects.get(id=request.user.id)

        inputvalue = request.POST['amount']
        if int(inputvalue)<0:
            return HttpResponse(status=404)
        
        currentuserobject.balance += int(inputvalue)
        currentuserobject.save()
        return HttpResponse(status=204,headers={'HX-Trigger':'fundsAdded'})
    
    else:
        return render(request,"app1/addfunds.html")
    

def withdrawfunds(request):
        
    if request.method=="POST":
        currentuserobject = get_user_model().objects.get(id=request.user.id)
        
        inputvalue = request.POST['amount']
        if int(inputvalue)< 0 or int(inputvalue)>currentuserobject.balance:
            return HttpResponse(status=404)
        
        currentuserobject.balance-= int(inputvalue)
        currentuserobject.save()
        return HttpResponse(status=204,headers={'HX-Trigger':'fundsWithdrew'})
     
    else:
        return render(request,"app1/withdrawfunds.html")






