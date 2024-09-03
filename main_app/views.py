from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.views import LoginView # type: ignore
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .forms import FeedingForm, FoodItemForm, CreateUserForm
from .models import Profile, Feeding, FoodItem
from . import utils
import os
import requests


import requests
import os
from dotenv import load_dotenv


load_dotenv()
# API_KEY = os.getenv('API_KEY')
# API = 'https://api.api-ninjas.com/v1/nutrition'
# response = requests.get(API, headers={'X-Api-Key': 'API_KEY'})


# Create your views here.
class Home(LoginView):
    template_name = 'home.html'
# def Home(request):
#     return HttpResponse('Hello World')

@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    feedings = Feeding.objects.filter(profile=profile).order_by('-date')[:1]
    if request.method == 'POST':
          feeding_form = FeedingForm(request.POST)
          food_item_form = FoodItemForm(request.POST)
          
          if feeding_form.is_valid() and food_item_form.is_valid():
               feeding = feeding_form.save(commit=False)
               feeding.profile = profile
               feeding.save()

               food_item = food_item_form.save(commit=False)
               food_item.feeding = feeding
               food_item.save()
               return redirect('dashboard')
    else:
        feeding_form = FeedingForm()
        food_item_form = FoodItemForm()
    
    context = {
         'profile': profile,
         'feedings': feedings,
         'feeding_form': feeding_form,
         'food_item_form': food_item_form,
    }
    return render(request, 'profile/dashboard.html', context)


def signup(request):
    error_message = ''
    form = CreateUserForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            print('Form is valid.')
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            print('Error:', form.errors)
            error_message = 'Invalid sign up - try again'

    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

def nutrition_view(request):
        food_item = request.GET.get('food', 'eggs')
        nutrtition_data = utils.get_nutrition_data(food_item)
        return JsonResponse(nutrtition_data)