import json
import requests_cache
import requests
from django.http import JsonResponse
from http import HTTPStatus

requests_cache.install_cache('cache1', expire_after=1800)
API_KEY = "CG-Sy2oZ9vfitdLYFbKGWQeb7Np"

def getcoinlist():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
    parameters = {
    'per_page':'250'
    }   
    headers = {
    'Accepts': 'application/json',
    'x-cg-demo-api-key': API_KEY,
    }
    try:
        response = requests.get(url,params=parameters,headers=headers)
        response.raise_for_status()
        data = response.json()
        return {'success':True,'data':data}

    except requests.exceptions.RequestException as error: 
        return {'success': False, 'error': str(error)}


def getcoin(coin):
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    parameters = {
    'ids':coin,
    }   
    headers = {
    'Accepts': 'application/json',
    'x-cg-demo-api-key': API_KEY,
    }
    try:
        response = requests.get(url,params=parameters,headers=headers)
        response.raise_for_status()
        data = response.json()
        return {'success':True,'data':data}

    except requests.exceptions.RequestException as error: 
        return {'success': False, 'error': str(error)}
    

def gettrendingcoins():
    url = 'https://api.coingecko.com/api/v3/search/trending'  
    headers = {
    'Accepts': 'application/json',
    'x-cg-demo-api-key': API_KEY,
    }
    try:
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        data = response.json()
        return {'success':True,'data':data}

    except requests.exceptions.RequestException as error: 
        return {'success': False, 'error': str(error)}
    

def getcoinchart(coin,days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd"
    parameters = {
    'days':str(days),
    'interval':''
    }   
    headers = {
    'Accepts': 'application/json',
    'x-cg-demo-api-key': API_KEY,
    }

    try:
        response = requests.get(url,params=parameters,headers=headers)
        response.raise_for_status()
        data = response.json()
        return {'success':True,'data':data}

    except requests.exceptions.RequestException as error: 
        return {'success': False, 'error': str(error)}
    
def getcoinprice(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"

    headers = {
    'Accepts': 'application/json',
    'x-cg-demo-api-key': API_KEY,
    }

    try:
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        data = response.json()
        return {'success':True,'data':data}

    except requests.exceptions.RequestException as error: 
        return {'success': False, 'error': str(error)}

