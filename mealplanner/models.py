from django.db import models
from django.conf import settings

class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    is_public = models.BooleanField(default=False)
    meal_name = models.CharField(max_length=200)
    meal_type = models.CharField(max_length=50, choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snack', 'Snack')])
    ingredients = models.TextField()
    calories = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.meal_name} ({self.meal_type})"