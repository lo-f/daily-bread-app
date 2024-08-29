from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
    ('S', 'Snack')
)

class Profile(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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

