# social/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

# Import your custom models
from .models import Post, Follow 


# ----------------------------------------------------------------------
# Authentication Views
# ----------------------------------------------------------------------

# Register View
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect("login")

    return render(request, "register.html")


# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# ----------------------------------------------------------------------
# Core App Views
# ----------------------------------------------------------------------

@login_required
def home_view(request):
    # 1. Retrieve all posts, ordered by newest first
    posts = Post.objects.all().order_by("-created_at")
    
    # 2. Get usernames of users the current user is following (for UI purposes)
    following_usernames = Follow.objects.filter(follower=request.user).values_list("followed__username", flat=True)

    return render(request, "home.html", {
        "posts": posts,
        "following_usernames": list(following_usernames), 
    })


def profile(request):
    return render(request, 'profile.html')


def another(request):
    return render(request, "another.html")


# ----------------------------------------------------------------------
# API/Action Views (Follow/Unfollow Logic)
# ----------------------------------------------------------------------
# social/views.py (or your_app/views.py)

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# <-- ADD THIS LINE -->
from django.views.decorators.csrf import csrf_exempt 

import json
from .models import Follow # Make sure this import is correct

# ... other views ...

@login_required
@require_POST
@csrf_exempt # Now defined
def toggle_follow(request):
    # ... rest of your toggle_follow logic ...
    # (The logic for creating/deleting Follow objects is correct)
    try:
        data = json.loads(request.body)
        followed_username = data.get('username')
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

    followed_user = get_object_or_404(User, username=followed_username)
    follower_user = request.user

    if follower_user == followed_user:
        return JsonResponse({'status': 'error', 'message': 'Cannot follow yourself'}, status=400)

    try:
        follow_instance = Follow.objects.get(follower=follower_user, followed=followed_user)
        follow_instance.delete()
        is_following = False
        message = 'Unfollowed successfully'
    except Follow.DoesNotExist:
        Follow.objects.create(follower=follower_user, followed=followed_user)
        is_following = True
        message = 'Followed successfully'

    return JsonResponse({
        'status': 'success',
        'is_following': is_following,
        'message': message
    })