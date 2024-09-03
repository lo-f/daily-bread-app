from django import forms
from .models import Feeding, FoodItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ['date', 'meal']
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            ),
        }

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = [
            'name',
            'calories',
            'fats',
            'proteins',
            'carbs'
        ]

class CreateUserForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True, help_text='First and Last name')
    age = forms.IntegerField(min_value=1, required=True,help_text='Enter your age')
    height = forms.FloatField(required=True, help_text='Height in inches')
    weight = forms.FloatField(required=True, help_text='Weight in pounds')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'name',
            'age',
            'height',
            'weight',
        ]
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            Profile.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                age=self.cleaned_data['age'],
                height=self.cleaned_data['height'],
                weight=self.cleaned_data['weight']
            )
        return user