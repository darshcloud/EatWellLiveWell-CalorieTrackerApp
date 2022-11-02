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
        
@login_required
def foodlist(request):
    food_items = Food_Obj.objects.all()
    for food in food_items:
        food.image = food.get_images.first()
    page = request.GET.get('page', 1)
    paginator = Paginator(food_items, 4)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'categories': Food_Cat.objects.all(),
        'foods': food_items,
        'pages': pages,
        'title': 'Food List'
    })


   

@login_required
def foodadd(request):
    ImageFormSet = forms.modelformset_factory(Image, form=ImageForm, extra=1)
    if request.method == 'POST':
        food_form = FoodForm(request.POST, request.FILES)
        image_form = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if food_form.is_valid() and image_form.is_valid():
            new_food = food_form.save(commit=False)
            new_food.save()

            for food_form in image_form.cleaned_data:
                if food_form:
                    image = food_form['image']
                    new_image = Image(food=new_food, image=image)
                    new_image.save()
                    

            return render(request, 'food_add.html', {
                'categories': Food_Cat.objects.all(),
                'food_form': FoodForm(),
                'image_form': ImageFormSet(queryset=Image.objects.none()),
                'success': True
            })
        
        else:
            return render(request, 'food_add.html', {
                'categories': Food_Cat.objects.all(),
                'food_form': FoodForm(),
                'image_form': ImageFormSet(queryset=Image.objects.none()),
            })

    else:
        return render(request, 'food_add.html', {
            'categories': Food_Cat.objects.all(),
            'food_form': FoodForm(),
            'image_form': ImageFormSet(queryset=Image.objects.none()),
            #'image_form': ImageForm(),
        })
def fooddetails(request, food_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    food = Food_Obj.objects.get(id=food_id)

    return render(request, 'food.html', {
        'categories': Food_Cat.objects.all(),
        'food': food,
        'images': food.get_images.all(),
    })
 
    

        



