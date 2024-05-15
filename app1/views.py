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
from .models import Order,Portfolio
from django.contrib.auth import get_user_model
from decimal import Decimal
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
    
def orders(request):

    orders = Order.objects.filter(user=request.user).order_by('-date')

    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"orders":orders,
               "page_obj":page_obj}
    
    return render(request,'app1/orders.html',context)

def portfolio(request):
    portfoliocoins = Portfolio.objects.filter(user=request.user)
    context = {'coins':portfoliocoins}
    return render(request,'app1/portfolio.html',context)
    
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


        if request.method =="POST":

            try:
                response = getcoin(coin)
                if response['success']:
                    response = response['data'][0]
                    date = response['last_updated']
                    dt = datetime.fromisoformat(date.rstrip("Z"))
                    date = dt.strftime("%B %d, %Y, %I:%M %p")

                else:
                    messages.error(request,"Error fetching coin data")
                    return(redirect("index"))
            except IndexError:
                messages.error(request,"Error fetching coin data")
                return(redirect("index"))


            currentprice = response['current_price']
            request.session['currentprice'] = currentprice
            request.session.modified = True
            
            if request.POST['action'] == "buy":

                coinname = request.POST['coinname']
                buyamount = request.POST['buyamount']
                buyamountusd = request.POST['buyamountusd']
                

                buyamount = Decimal(str(buyamount))
        
                if Portfolio.objects.filter(user=request.user,coin=coinname).exists():
                    portfolio = Portfolio.objects.get(user=request.user,coin=coinname)
                    portfolio.amount += buyamount
                    
                else:
                    portfolio = Portfolio(user=request.user,coin=coinname)
                    portfolio.amount += buyamount

                # Subtract from balance
                
                request.user.balance -= Decimal(buyamountusd)
                request.user.save()
            
                portfolio.save()
                newOrder = Order(user=request.user,action="BUY",coin=coinname,price=currentprice,amount=buyamount)
                newOrder.save()

                return redirect(f"/coin/{coinname.lower()}")
            

            if request.POST['action'] == "sell":
                coinname = request.POST['coinname']
                sellamount = request.POST['sellamount']
                sellamountusd = request.POST['sellamountusd']
                sellamount = Decimal(str(sellamount))
        
                if Portfolio.objects.filter(user=request.user,coin=coinname).exists():
                    portfolio = Portfolio.objects.get(user=request.user,coin=coinname)
                    portfolio.amount -= sellamount
                    
                else:
                    portfolio = Portfolio(user=request.user,coin=coinname)
                    portfolio.amount -= sellamount

                #add to balance
                request.user.balance += Decimal(sellamountusd)
                request.user.save()
        
                portfolio.save()
                newOrder = Order(user=request.user,action="SELL",coin=coinname,price=currentprice,amount=sellamount)
                newOrder.save()
                
                return redirect(f"/coin/{coinname.lower()}")
        else:
            if request.user.is_authenticated:
                allOrders = Order.objects.filter(user=request.user,coin=coin).order_by('-date')
                try:
                    coinAmount = Portfolio.objects.get(user=request.user, coin=coin).amount
                except Portfolio.DoesNotExist:
                    coinAmount = 0

            try:
                response = getcoin(coin)
                if response['success']:
                    response = response['data'][0]
                    date = response['last_updated']
                    dt = datetime.fromisoformat(date.rstrip("Z"))
                    date = dt.strftime("%B %d, %Y, %I:%M %p")

                    context = {"coin":response,
                                "date":date
                                }
                    if request.user.is_authenticated:
                        context['orders']=allOrders
                        context['coinamount']=coinAmount
                        
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
        if float(inputvalue)<0:
            return HttpResponse(status=404)
        
        print(Decimal(inputvalue))
        currentuserobject.balance += Decimal(inputvalue)
        currentuserobject.save()
        return HttpResponse(status=204,headers={'HX-Trigger':'fundsAdded'})
    
    else:
        return render(request,"app1/addfunds.html")
    

def withdrawfunds(request):
        
    if request.method=="POST":
        currentuserobject = get_user_model().objects.get(id=request.user.id)
        
        inputvalue = request.POST['amount']
        if float(inputvalue)< 0 or Decimal(inputvalue)>currentuserobject.balance:
            return HttpResponse(status=404)
        
        currentuserobject.balance-= Decimal(inputvalue)
        currentuserobject.save()
        return HttpResponse(status=204,headers={'HX-Trigger':'fundsWithdrew'})
     
    else:
        return render(request,"app1/withdrawfunds.html")






