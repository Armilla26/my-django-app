from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages, admin
from django.http import HttpResponse
from django.db import models
from .models import Meal

def check_admin_registration(request):
    registered_models = [model.__name__ for model, model_admin in admin.site._registry.items()]
    return HttpResponse(f"Registered models: {', '.join(registered_models)}")

@login_required
def dashboard(request):
    if request.method == 'POST':
        meal_name = request.POST['mealName']
        meal_type = request.POST['mealType']
        ingredients = request.POST['ingredients']
        calories = request.POST['calories']
        if not all([meal_name, meal_type, ingredients, calories]) or int(calories) > 5000 or int(calories) <= 0:
            messages.error(request, "Please fill all fields with valid data (calories 1-5000).")
        else:
            Meal.objects.create(user=request.user, meal_name=meal_name, meal_type=meal_type, ingredients=ingredients, calories=calories)
            return redirect('mealplanner:dashboard')
    meals = Meal.objects.filter(models.Q(user=request.user) | models.Q(is_public=True)).order_by('meal_type')
    total_calories = sum(meal.calories for meal in meals)
    return render(request, 'mealplanner/dashboard.html', {'meals': meals, 'total_calories': total_calories})

@login_required
def edit_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id, user=request.user)
    if request.method == 'POST':
        meal_name = request.POST['mealName']
        meal_type = request.POST['mealType']
        ingredients = request.POST['ingredients']
        calories = request.POST['calories']
        if not all([meal_name, meal_type, ingredients, calories]) or int(calories) > 5000 or int(calories) <= 0:
            messages.error(request, "Calories must be between 1 and 5000.")
        else:
            meal.meal_name = meal_name
            meal.meal_type = meal_type
            meal.ingredients = ingredients
            meal.calories = calories
            meal.save()
            return redirect('mealplanner:dashboard')
    return render(request, 'mealplanner/edit_meal.html', {'meal': meal})

@login_required
def delete_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id, user=request.user)
    if request.method == 'POST':
        meal.delete()
        return redirect('mealplanner:dashboard')
    return render(request, 'mealplanner/delete_meal.html', {'meal': meal})