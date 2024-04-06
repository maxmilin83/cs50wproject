import json
import requests_cache
import requests

requests_cache.install_cache('cache1', expire_after=1800)


def getcoinlist():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'500',
    'convert':'USD'
    }   
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '23f9ebe7-869d-4006-8c74-2c96c6a2a66a',
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
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters = {
    'id':coin,
    }   
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '23f9ebe7-869d-4006-8c74-2c96c6a2a66a',
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