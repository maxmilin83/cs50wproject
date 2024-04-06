import json
import requests_cache
import requests
from django.http import JsonResponse
from http import HTTPStatus

requests_cache.install_cache('cache1', expire_after=1800)


def getcoinlist():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
    parameters = {
    'per_page':'250'
    }   
    headers = {
    'Accepts': 'application/json',
    'x-cg-demo-api-key': 'CG-zFXFvrLdMqDSM3og6f6r1qZa',
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
    'x-cg-demo-api-key': 'CG-zFXFvrLdMqDSM3og6f6r1qZa',
    }
    try:
        response = requests.get(url,params=parameters,headers=headers)
        response.raise_for_status()
        data = response.json()
        return {'success':True,'data':data}

    except requests.exceptions.RequestException as error: 
        return {'success': False, 'error': str(error)}
    

