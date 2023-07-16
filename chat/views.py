from django.shortcuts import render
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse



# from .serializers import *
# from rest_framework import viewsets, permissions
# from rest_framework_simplejwt.views import TokenObtainPairView


def index(request):
    users = UserAuth.objects.all()
    auth_user = request.user
    return render(request, 'chat/chatroom.html',{
        'users': users,
        'auth_user': auth_user,
    })
    # return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, "chat/room.html", {
        "room_name": room_name
        }
    )

def login_page(request):
    return render(request, 'chat/login.html',{
        
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'chat/login.html',{
                'login_message':'نام کاربری و یا رمز عبور نامعتبر است'
            })

def register_page(request):
    return render(request, 'chat/register.html',{

    })


def user_registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        username_exists = UserAuth.objects.values_list('username', flat=True)
        
        if confirmation != password:
            return render(request, 'chat/register.html',{
                'message': ' !رمز عبور مطابقت ندارد, لطفا دوباره وارد کنید',
            })  
        elif username in username_exists is not None:
            return render(request, 'chat/register.html',{
                'username_exists_message': 'کاربری با این نام کاربری از قبل وجود دارد',
            })  
        else:
            user = UserAuth.objects.create_user(username,password)
            user.save()
            return HttpResponseRedirect(reverse('index'))
        
    else:
        return render(request, 'chat/register.html')



def logout_user(request):
    logout(request)

    return redirect('index')
