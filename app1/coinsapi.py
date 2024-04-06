import json
import requests_cache
import requests

requests_cache.install_cache('cache1', expire_after=1800)


def getcoinlist():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
    #&per_page=250
    parameters = {
    'per_page':'250'
    }   
    headers = {
    'Accepts': 'application/json',
    'x-cg-demo-api-key': 'CG-zFXFvrLdMqDSM3og6f6r1qZa',
    }
    try:
        response = requests.get(url,params=parameters,headers=headers)

        if response.status_code==200:

            data = response.json()
            return data
        else:
            return {'error':f'Failed to fetch data {response.status_code}'}
    except Exception:
        return {'error':'Error occured','details':str(Exception)}
    


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

        if response.status_code==200:

            data = response.json()
            return data
        else:
            return {'error':f'Failed to fetch data {response.status_code}'}
    except Exception:
        return {'error':'Error occured','details':str(Exception)}