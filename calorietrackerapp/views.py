from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Food_Obj, Food_Cat, Food_log_mdl, Image, UserWeight
from .forms import FoodForm, ImageForm


def index(request):
    return foodlist(request)


def login_v(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('food_list'))
        else:
            return render(request, 'login.html', {
                'message': 'Incorrect username/password combination'
            })
    else:
        return render(request, 'login.html',  {
        })


def logout_v(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'register.html', {
                'message': 'Passwords must match.',
                'categories': Food_Cat.objects.all()
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                'message': 'Username already taken.',
                'categories': Food_Cat.objects.all()
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'register.html', {
            'categories': Food_Cat.objects.all()
        })

