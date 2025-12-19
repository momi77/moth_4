from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from users.models import Profile



def register_view(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "users/register.html", context={"form": form})
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "users/register.html", context={"form": form})
        form.cleaned_data.__delitem__('password_confirm')
        avatar = form.cleaned_data.pop("avatar")
        age = form.cleaned_data.pop("age")
        user = User.objects.create(**form.cleaned_data)
        if user:
            Profile.objects.create(user=user,avatar=avatar, age=age)
        return redirect("/")


def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "users/login.html", context={"form": form})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "users/login.html", context={"form": form})
        user = authenticate(**form.cleaned_data)
        if user:
            login(request, user)
        return redirect("/")
        

@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect("/")        


@login_required(login_url="/login/")
def profile_view(request):
    if request.method == "GET":
        user = request.user
        profile = user.profile
        posts = user.posts.all( )
        if profile:
            return render(request, "users/profile.html", context={"user": user, "posts": posts})
        else:
            return redirect("/")