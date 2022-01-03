from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http.response import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import *

"""


TODO
FIQUEI NA PARTE DE EDITAR POSTS.
    FALTA TUDO, SO ADICIONEI O "BOTAO".


"""

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

@login_required(login_url='/register')
def following(request, page=0):
    if page == 0:
        return HttpResponseRedirect('/following/1')
    results = {}
    
    try:
        posts = Post.objects.filter(user__in=list(Follow.objects.filter(follower=request.user).values_list('id', flat=True))).order_by('-date')
        p = Paginator(posts, 10)
        results["posts"] = p.page(page)
        results["posts_numpages"] = p.num_pages
        results["posts_currpage"] = page
    except:
        pass

    return render(request, "network/index.html", results)


def index(request, page=0):
    if page == 0:
        return HttpResponseRedirect('/1')

    results = {}
    if request.method == "POST" and request.user.is_authenticated:
        try:
            post = request.POST["newPost"]
            newPost = Post(post=post, user=request.user)
            newPost.save()
        except:
            pass

    try:
        posts = Post.objects.filter().order_by('-date')
        p = Paginator(posts, 10)
        results["posts"] = p.page(page)
        results["posts_numpages"] = p.num_pages
        results["posts_currpage"] = page
    except:
        pass

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

@login_required(login_url='/register')
def post(request, id):
    try:
        post = Post.objects.get(id=id)
    except:
        return HttpResponseNotFound("404 - Not found")
        
    if post.user != request.user:
        return HttpResponseForbidden("403 - Forbidden")

    if request.method == "POST":
        post.post = request.POST["editPost"]
        post.save()

    return JsonResponse({"status: success"})