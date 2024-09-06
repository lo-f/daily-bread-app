import os
import requests
from django.http import JsonResponse
import json

def get_instant_data(query):
    API_ID = os.getenv('API_ID')
    API_KEY = os.getenv('API_KEY')
    API_BASE_URL = "https://trackapi.nutritionix.com/v2/search/instant"
    url = API_BASE_URL
    headers = {
        'x-app-id': API_ID,
        'x-app-key': API_KEY,
        'Content-type': 'application/json'
    }
    payload = {
        'query': query
    }

    response = requests.get(url, headers=headers, json=payload)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return {'error': 'Failed to fetch data', 'status_code': response.status_code}


def get_nutrition_data(query):
    API_ID = os.getenv('API_ID')
    API_KEY = os.getenv('API_KEY')
    API_BASE_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    url = API_BASE_URL
    headers = {
        'x-app-id': API_ID,
        'x-app-key': API_KEY,
        'Content-type': 'application/json'
    }
    payload = {
        'query': query
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return {'error': 'Failed to fetch data', 'status_code': response.status_code}

