from django.urls import path
from . import views

app_name = 'mealplanner'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('edit/<int:meal_id>/', views.edit_meal, name='edit_meal'),
    path('delete/<int:meal_id>/', views.delete_meal, name='delete_meal'),
    path('check-admin/', views.check_admin_registration, name='check-admin'),
]