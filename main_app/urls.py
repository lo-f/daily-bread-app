from django.urls import path
from . import views

urlpatterns = [
    # path('', views.Home.as_view(), name='home'),
    path('', views.Home.as_view(), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('get-nutrition-data/', views.nutrition_view, name='nutrition_view'),


    path('accounts/signup/', views.signup, name='signup'),

]