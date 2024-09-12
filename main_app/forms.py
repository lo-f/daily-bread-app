from django import forms
from django.forms import formset_factory, inlineformset_factory
from .models import Feeding, FoodItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now().date()

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = [
            'name',
            'calories',
            'fats',
            'proteins',
            'carbs',
            'photo_url',
        ]
        widgets = {
            'photo_url': forms.HiddenInput() 
        }

FoodItemFormSet = inlineformset_factory(
    Feeding, FoodItem,
    form=forms.ModelForm,
    fields=['name', 'calories', 'fats', 'proteins', 'carbs', 'photo_url'],
    widgets = {
            'photo_url': forms.HiddenInput()  
    },
    extra=1,
    can_delete=True
)


class CreateUserForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True, help_text='First and Last name')
    age = forms.IntegerField(min_value=1, required=True, help_text='Enter your age')
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
            print(f"Form is valid: {self.is_valid()}")
            print(f"Cleaned data: {self.cleaned_data}")
            user.save()
            
        else:
            print("Some fields are missing in cleaned data")
        return user