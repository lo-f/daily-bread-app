from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import FeedingForm, FoodItemFormSet, CreateUserForm, FoodItemForm
from .models import Profile, Feeding, FoodItem
from .utils import get_nutrition_data, get_instant_data
import os
import requests


import requests
import os
from dotenv import load_dotenv


load_dotenv()



# Create your views here.
class Home(LoginView):
    template_name = 'home.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')
# def Home(request):
#     return HttpResponse('Hello World')

@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    feedings = Feeding.objects.filter(profile=profile).order_by('-date')
    
    # Calculate total calories for the current day
    today = timezone.now().date()
    daily_calories = FoodItem.objects.filter(
        meal__profile=profile, meal__date=today
    ).aggregate(total_calories=Sum('calories'))['total_calories'] or 0
    food_items_today = FoodItem.objects.filter(meal__profile=profile, meal__date=today)
    nutrition_totals = food_items_today.aggregate(
        total_fats=Sum('fats'),
        total_proteins=Sum('proteins'),
        total_carbs=Sum('carbs')
    )

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
         'daily_calories': daily_calories,
         'nutrition_totals': nutrition_totals,
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

@login_required
def update_feeding(request, pk):
    feeding = get_object_or_404(Feeding, pk=pk)

    FoodItemFormSet = inlineformset_factory(
        Feeding, FoodItem, form=FoodItemForm, extra=1, can_delete=True
    )

    if request.method == "POST":
        feeding_form = FeedingForm(request.POST, instance=feeding)
        food_item_formset = FoodItemFormSet(
            request.POST, instance=feeding, prefix="fooditem"
        )

        if feeding_form.is_valid() and food_item_formset.is_valid():
            feeding_form.save()
            food_item_formset.save()
            return redirect("meal-detail", feeding_id=feeding.pk)
    else:
        feeding_form = FeedingForm(instance=feeding)
        food_item_formset = FoodItemFormSet(instance=feeding, prefix="fooditem")

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

# def nutrition_view(request):
#     if request.method == 'GET':
#         query = request.GET.get('query', '')
#         if query:
#             nutrition_data = get_nutrition_data(query)
#             return JsonResponse(nutrition_data)
#         else:
#             return JsonResponse({'error': 'No query provided.'}, status=400)

@csrf_exempt  # Allows AJAX POST requests without CSRF token (ensure security in production)
def nutrition_view(request):
    if request.method == "POST":
        selected_food = request.POST.get("selection", "")
        if not selected_food:
            return JsonResponse({"error": "No selection provided"}, status=400)

        try:
            data = get_nutrition_data(selected_food)  # Fetch detailed nutrition data
            if "error" in data:
                return JsonResponse({"error": data["error"]}, status=500)
            return JsonResponse(data, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_instant_data_view(request):
    query = request.GET.get("query", "")
    if not query:
        return JsonResponse({"error": "No query provided."}, status=400)

    try:
        data = get_instant_data(query)
        if "error" in data:
            return JsonResponse({"error": data["error"]}, status=500)
        return JsonResponse({"foods": data["common"]}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)