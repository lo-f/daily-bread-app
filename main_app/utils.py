import os
import requests
from django.http import JsonResponse
import json


def get_nutrition_data(request):
    API_ID = os.getenv('API_ID')
    API_KEY = os.getenv('API_KEY')
    API_BASE_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    url = API_BASE_URL
    headers = {
        'x-app-id': API_ID,
        'x-app-key': API_KEY,
        'Content-type': 'application/json'
    }
    query = {
        'query': 'eggs'
    }

    response = requests.post(url, headers=headers, json=query)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return {'error': 'Failed to fetch data', 'status_code': response.status_code}
    # new_string = json.dumps(data,indent=2)
    # print(new_string)
    # return JsonResponse(response.json())
    # for food in data['foods']:
    #     name = food['food_name']
    #     serving_size = food['serving_qty']
    #     cal = food['nf_calories']
    #     print(name, serving_size, cal)
# get_nutrition_data('POST')





# def get_data_from_api(endpoint):
#     url = f"{API_BASE_URL}/{endpoint}"
#     headers = {
#         "Authorization": f"Bearer {API_ID}"
#     }
    
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()  # Raise an error for bad responses
#     return response.json()

# import requests

# print(settings.API_ID)
# print(settings.API_KEY)

# API_BASE_URL = 'https://trackapi.nutritionix.com/v2/natural/nutrients'

# def get_authenticated_headers():
#     """Generate headers required for the API request."""
#     return {
#         "Authorization": f"Bearer {settings.API_ID}",
#         "Content-Type": "application/json",
#     }

# def fetch_data_from_api(endpoint):
#     """Fetch data from the third-party API."""
#     url = f"{API_BASE_URL}/{endpoint}"
#     headers = get_authenticated_headers()
    
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"API request failed: {e}")
#         return None

# def options(request):
#     import json
#     import requests
#     if request.method == 'POST':
#         query = request.POST['query']
#         api_url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
#         api_request = requests.get (
#             api_url + query,
#             headers = {
#                 'Content-Type': 'application/json',
#                 'x-app-id': 'cf6bdb82',
#                 'x-app-key': '66b931289f45aff91db594e06d2878f4'
#             })
#         try:
#             api = json.loads(api_request.content)
#             print(api_request.content)
#         except Exception as e:
#             api = 'oops! There was an error'
#             print(e)
#         return render(request, 'home.html',{'api':api})
#     else:
#         return render(request, 'home.html',{'query':'Enter a valid query'})


# def options = {
#   'method': 'POST',
#   'url': 'https://trackapi.nutritionix.com/v2/natural/nutrients',
#   'headers': {
#     'Content-Type': 'application/json',
#     'x-app-id': ,
#     'x-app-key':
#   },
#   body: JSON.stringify({
#     "query": "grape"
#   })