from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
    ('S', 'Snack')
)

class Profile(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    height = models.FloatField(help_text='Height in inches')
    weight = models.FloatField(help_text='Weight in pounds')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Feeding(models.Model):
    date = models.DateField('Feed Date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"
    class Meta:
        ordering = ['-date']

class FoodItem(models.Model):
    meal = models.ForeignKey(Feeding, on_delete=models.CASCADE, related_name='food_item')
    name = models.CharField(max_length=100)
    calories = models.FloatField()
    fats = models.FloatField()
    proteins = models.FloatField()
    carbs = models.FloatField()

    def __str__(self):
        return self.name