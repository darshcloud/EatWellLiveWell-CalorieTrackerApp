from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from . import decode_jwt
from django.shortcuts import render
from decouple import config
import base64
import requests
import boto3
from calorietrackerprj import settings
from difflib import SequenceMatcher

from .models import User, Food_Obj, Food_Cat, Food_log_mdl, Image, UserWeight
from .forms import FoodForm, ImageForm


def index(request):
    return foodlist(request)

def login_v(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == "" or password == "":
            return render(request, 'login.html', {
                'message': 'Username/Password cannot be empty'
            })
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('food_list'))
        else:
            return render(request, 'login.html', {
                'message': 'Incorrect username/password combination'
            })
    else:
        try:
            code = request.GET.get('code')
            # print(code)
            userData = getTokens(code)
            # print(userData)
            context = {'name': userData['name'], 
                        'email': userData['email'],
                        'token': userData['token'],
                        'status': 1,}
            # print(context)
            try:
                user = User.objects.create_user(context['name'], context['email'], context['token'])
                user.save()
            except Exception:
                print("User Create Failed")
                pass
            try:
                user = authenticate(request, username=context['name'], password=context['token'])
            except Exception:
                print("user auth failed")
                pass
            print(user)
            response = render(request, 'login.html' , context)
            response.set_cookie('sessiontoken', userData['id_token'], max_age=60*60*24, httponly=True)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('food_list'))
            else:
                return render(request, 'login.html', {
                    'message': 'Incorrect username/password combination'
                })
        except Exception as e:
            token = getSession(request)
            if token is not None:
                userData = decode_jwt.lambda_handler({'token':token}, None)
                context = {'name': userData['name'], 
                        'email': userData['email'],
                        'status': 1,}
                # print(context)
                render(request, 'login.html' , context)
            print("No code")
            return render(request, 'login.html', {'status': 0})

def logout_v(request):
    logout(request)  
    response =  render(request, 'login.html', {'status': 0}) 
    response.delete_cookie('sessiontoken')
    return HttpResponseRedirect(reverse('login'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if username == "" or email == "" or password == "" or confirmation == "":
            return render(request, 'register.html', {
                'message': 'Username/Email/Password fields are Empty',
                'categories': Food_Cat.objects.all()
            })
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
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY

            dynamodb = boto3.resource('dynamodb',region_name='us-east-1',aws_access_key_id=aws_access_key_id , aws_secret_access_key=aws_secret_access_key )
            table = dynamodb.Table('fooditems')

            response = table.put_item(
                Item={
                    'foodname': new_food.food_name,
                    'calorie': new_food.calories
                }
            )

            print(response)

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


@login_required
def foodlogview(request):
    message = ''
    if request.method == 'POST':
        request_file = request.FILES['document'] if 'document' in request.FILES else None
        if request_file:
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            client=boto3.client('rekognition',region_name=settings.REGION_NAME,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key )
            response = client.detect_labels(Image={'Bytes': request_file.read()})
            foods = Food_Obj.objects.all()
            done = False
            for label in response['Labels']:
                name = label['Name']
                for food in foods:
                    if done:
                        break
                    s = SequenceMatcher(None, food.food_name, name)
                    if s.ratio() > 0.75 and Food_Obj.objects.filter(food_name=food.food_name).exists():
                        print(food)
                        user = request.user
                        food_log = Food_log_mdl(user=user, food_consumed=food)
                        food_log.save()
                        done = True
                        message = "successfully added " + food.food_name
                if done:
                    break

            if not done:
                message = 'no match found for the image you have inserted. please use the drop down instead'

        else:   
            food = request.POST['food_consumed']
            food_consumed = Food_Obj.objects.get(food_name=food)
            user = request.user
            food_log = Food_log_mdl(user=user, food_consumed=food_consumed)
            food_log.save()
    foods = Food_Obj.objects.all()
    user_food_log = Food_log_mdl.objects.filter(user=request.user)

    return render(request, 'food_log.html', {
        'categories': Food_Cat.objects.all(),
        'foods': foods,
        'user_food_log': user_food_log,
        'message': message,
    })


def categories(request):
    return render(request, 'categories.html', {
        'categories': Food_Cat.objects.all()
    })

    

def categorydetails(request, category_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    category = Food_Cat.objects.get(category_name=category_name)
    foods = Food_Obj.objects.filter(category=category)

    for food in foods:
        food.image = food.get_images.first()
    page = request.GET.get('page', 1)
    paginator = Paginator(foods, 4)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'food_category.html', {
        'categories': Food_Cat.objects.all(),
        'foods': foods,
        'foods_count': foods.count(),
        'pages': pages,
        'title': category.category_name
    })


@login_required
def weightlog(request):
    if request.method == 'POST':
        user_weight = request.POST['weight']
        entry_date = request.POST['date']
        user_name = request.user
        weight_log = UserWeight(user_name=user_name, user_weight=user_weight, entry_date=entry_date)
        weight_log.save()
    userweightlog = UserWeight.objects.filter(user_name=request.user)

    return render(request, 'user_profile.html', {
        'categories': Food_Cat.objects.all(),
        'user_weight_log': userweightlog
    })


@login_required
def weightlogdelete(request, weight_id):
    weight_recorded = UserWeight.objects.filter(id=weight_id) 

    if request.method == 'POST':
        weight_recorded.delete()
        return redirect('weight_log')
    
    return render(request, 'weight_log_delete.html', {
        'categories': Food_Cat.objects.all()
    })


@login_required
def Food_log_mdldelete(request, food_id):
    food_consumed = Food_log_mdl.objects.filter(id=food_id)
    if request.method == 'POST':
        food_consumed.delete()
        return redirect('food_log')
    return render(request, 'food_log_delete.html', {
        'categories': Food_Cat.objects.all()
    })

def getTokens(code):
    TOKEN_ENDPOINT = config('TOKEN_ENDPOINT')
    REDIRECT_URI = config('REDIRECT_URI')
    CLIENT_ID = config('CLIENT_ID') 
    CLIENT_SECRET = config('CLIENT_SECRET')
    encodeData = base64.b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SECRET}", "ISO_8859-1")).decode("ascii")
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encodeData}'
    }

    body = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    # print(body)
    response = requests.post(TOKEN_ENDPOINT, data=body, headers=headers)
    # print("response", response)
    id_token = response.json()['id_token']
    userData = decode_jwt.lambda_handler({'token':id_token}, None)
    if not userData:
        return False 
    user = {
        'id_token': id_token,
        'name': userData['cognito:username'],
        'email': userData['email'],
        'token': userData['sub']
    }
    return user

def getSession(request):
    try:
        response = request.COOKIES["sessiontoken"]
    except:
        return None
