from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import Http404, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from .models import *

def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponseNotFound("404 - Not found")
    
    results = {}
   
    if request.method == "POST":
        if Follow.objects.filter(following = user, follower = request.user).count() > 0:
            f = Follow.objects.filter(following = user, follower = request.user)
            f.delete()
        else:
            f = Follow(following = user, follower = request.user)
            f.save()

    results['username'] = username
    results["posts"] = list(Post.objects.filter(user=user).order_by('-date'))
    results["followers"] = Follow.objects.filter(following = user).count()
    results["following"] = Follow.objects.filter(follower = user).count()
    results["iamfollowing"] = True if Follow.objects.filter(following = user, follower = request.user).count() > 0 else False

    return render(request, "network/profile.html", results)


def index(request):
    results = {}
    if request.method == "POST" and request.user.is_authenticated:
        try:
            post = request.POST["newPost"]
            newPost = Post(post=post, user=request.user)
            newPost.save()
        except:
            pass
    
    results["posts"] = list(Post.objects.filter().order_by('-date'))

    return render(request, "network/index.html", results)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
