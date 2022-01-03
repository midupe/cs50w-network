
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:page>", views.index, name="index"),
    path("user/<str:username>", views.profile, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("following/<int:page>", views.following, name="following"),
    path("post/<int:id>", views.post, name="post"),
    path("like/<int:id>", views.like, name="like"),
    path("likes", views.myLikes, name="myLikes")
]
