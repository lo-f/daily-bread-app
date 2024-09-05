from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponse, JsonResponse
from .forms import FeedingForm, FoodItemFormSet, CreateUserForm, FoodItemForm
from .models import Profile, Feeding, FoodItem
from . import utils
import os
import requests


import requests
import os
from dotenv import load_dotenv


load_dotenv()



# Create your views here.
class Home(LoginView):
    template_name = 'home.html'
# def Home(request):
#     return HttpResponse('Hello World')

@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    feedings = Feeding.objects.filter(profile=profile).order_by('-date')
    if request.method == 'POST':
        feeding_form = FeedingForm(request.POST)
        food_item_formset = FoodItemFormSet(request.POST, prefix='fooditem')
          
        if feeding_form.is_valid() and food_item_formset.is_valid():
            feeding = feeding_form.save(commit=False)
            feeding.profile = profile
            feeding.save()

            food_items = food_item_formset.save(commit=False)
            for food_item in food_items:
                food_item.meal = feeding
                food_item.save()
                print('food items saved')

            for form in food_item_formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()


            return redirect('dashboard')
    else:
        feeding_form = FeedingForm()
        food_item_formset = FoodItemFormSet(prefix='fooditem')
    
    context = {
         'profile': profile,
         'feedings': feedings,
         'feeding_form': feeding_form,
         'food_item_formset': food_item_formset,
    }
    return render(request, 'profile/dashboard.html', context)

@login_required
def meal_detail(request, feeding_id):
     feeding = Feeding.objects.get(id=feeding_id)
     feeding_form = FeedingForm()
     return render(request, 'profile/meal_detail.html', {
          'feeding': feeding,
          'feeding_form': feeding_form
     })

class MealDelete(LoginRequiredMixin, DeleteView):
     model = Feeding
     success_url = '/dashboard/'

def update_feeding(request, pk):
    # Get the Feeding instance or return 404
    feeding = get_object_or_404(Feeding, pk=pk)

    # Define the inline formset
    FoodItemFormSet = inlineformset_factory(
        Feeding, FoodItem, form=FoodItemForm, extra=1, can_delete=True
    )

    # Process the form on POST request
    if request.method == "POST":
        feeding_form = FeedingForm(request.POST, instance=feeding)
        food_item_formset = FoodItemFormSet(
            request.POST, instance=feeding, prefix="fooditem"
        )

        if feeding_form.is_valid() and food_item_formset.is_valid():
            # Save both feeding form and food items formset
            feeding_form.save()
            food_item_formset.save()
            return redirect("meal-detail", feeding_id=feeding.pk)
    else:
        # Initialize forms for GET request
        feeding_form = FeedingForm(instance=feeding)
        food_item_formset = FoodItemFormSet(instance=feeding, prefix="fooditem")

    # Render the template with the form and formset
    return render(
        request,
        "main_app/feeding_form.html",
        {
            "feeding_form": feeding_form,
            "food_item_formset": food_item_formset,
            "feeding": feeding,
        },
    )



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