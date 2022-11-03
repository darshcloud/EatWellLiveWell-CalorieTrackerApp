from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_v, name='index'),
    #path('', views.index, name='index'),
    path('login', views.login_v, name='login'),
    path('logout', views.logout_v, name='logout'),
    path('register', views.register, name='register'),
    path('profile/weight', views.weightlog, name='weight_log'),

    path('food/list', views.foodlist, name='food_list'),
    path('food/add', views.foodadd, name='food_add'),
    path('food/foodlog', views.foodlogview, name='food_log'),
    path('food/foodlog/delete/<int:food_id>', views.Food_log_mdldelete, name='food_log_delete'),

]