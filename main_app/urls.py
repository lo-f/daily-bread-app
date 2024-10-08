from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('meals/<int:feeding_id>/', views.meal_detail, name='meal-detail'),
    path('meals/<int:pk>/delete/', views.MealDelete.as_view(), name='meal-delete'),
    path('meals/<int:pk>/update/', views.update_feeding, name='meal-update'),

    path('get-instant-data/', views.get_instant_data_view, name='get-instant-data-view'),
    path('get-nutrition-data/', views.nutrition_view, name='nutrition-view'),


    path('accounts/signup/', views.signup, name='signup'),

]