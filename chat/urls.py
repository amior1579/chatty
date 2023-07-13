from django.urls import path, include
from . import views
# from rest_framework import routers
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('login_page', views.login_page, name='login_page'),
    path('register_page', views.register_page, name='register_page'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('user_registration', views.user_registration, name='user_registration'),
    path('user_login', views.user_login, name='user_login'),
    
    path("<str:room_name>/", views.room, name="room"),
]