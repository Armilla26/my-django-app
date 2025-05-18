from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import CustomUser

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('mealplanner:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        email = request.POST.get('email')

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/signup.html')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return render(request, 'accounts/signup.html')

        if not email:
            messages.error(request, "Email is required.")
            return render(request, 'accounts/signup.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'accounts/signup.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return render(request, 'accounts/signup.html')

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('mealplanner:dashboard')
    return render(request, 'accounts/signup.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')