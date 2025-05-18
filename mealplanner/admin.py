from django.contrib import admin
from .models import Meal
from django import forms

class MealAdminForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['user', 'meal_name', 'meal_type', 'ingredients', 'calories', 'is_public']
        exclude = ['created_at']  
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'created_at' in self.fields:
            del self.fields['created_at']

class MealAdmin(admin.ModelAdmin):
    form = MealAdminForm
    list_display = ('meal_name', 'meal_type', 'user', 'calories', 'is_public', 'created_at')
    list_filter = ('meal_type', 'user', 'is_public')
    search_fields = ('meal_name', 'ingredients')
    
    
    def get_form(self, request, obj=None, **kwargs):
        kwargs['fields'] = ['user', 'meal_name', 'meal_type', 'ingredients', 'calories', 'is_public']
        return super().get_form(request, obj, **kwargs)

admin.site.register(Meal, MealAdmin)