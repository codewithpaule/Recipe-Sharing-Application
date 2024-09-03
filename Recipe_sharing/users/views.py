# users/views.py

from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

def signup(request):
    if request.method == 'POST':
        # Retrieve form data using request.POST.get()
        username = request.POST.get('userName')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        password1 = request.POST.get('password')  # Change variable name to password1 to avoid conflicts

        if User.objects.filter(email=email).exists():
            error_message = 'Username already exists.'
            return render(request, 'users/sign-up.html', {'error_message': error_message})

        # Create user profile
        user = User.objects.create(username=username, email=email, password=make_password(password1))
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        UserProfile.objects.create(
            user=user,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            password=password1
        )

        # Redirect to home page or wherever you want after successful signup
        return redirect('signin')

    return render(request, 'users/sign-up.html')  # Render the signup form template

# users/views.py
@csrf_exempt
def signin(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is authenticated, log in the user
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
        else:
            # Authentication failed, render signin page with error message
            error_message = 'Invalid username or password.'
            return render(request, 'users/sign-in.html', {'error_message': error_message})

    return render(request, 'users/sign-in.html')  # Render the signin form template

def update_personal_information(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('userName')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        
        # Update user's profile
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()  # Save the changes to the User instance
        
        # Check if the user has a profile, and update the phone number if it exists
        if hasattr(user, 'profile'):
            user.profile.phone_number = phone_number
            user.profile.save()  # Save the changes to the UserProfile instance
        
        return redirect('manage')  # Redirect to the user's profile page
    
    return render(request, 'main/manage.html')

def change_password(request):
    user = request.user
    if request.method == 'POST':
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')
        
        # Check if new password matches confirm password
        if new_password == confirm_password:
            # Change user's password
            user.set_password(new_password)
            user.save()
            
            return redirect('signup')  # Redirect to the user's profile page
        
        # If passwords don't match, display an error message
        error_message = 'Passwords do not match.'
        return render(request, 'main/manage.html', {'error_message': error_message})
    
    return render(request, 'main/index.html')


def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the home page after logout
