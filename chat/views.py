from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.decorators import action

from rest_framework import viewsets, permissions
from .serializers import *
from django.db.models import Q
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin


# from .serializers import *
# from rest_framework import viewsets, permissions
# from rest_framework_simplejwt.views import TokenObtainPairView


# request_user = authenticate
# print(request_user)

def index(request):
    users = UserAuth.objects.all()
    auth_user = request.user
    return render(request, 'chat/contacts.html',{
        'users': users,
        'auth_user': auth_user,
    })
    # return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, "chat/room.html", {
        "room_name": room_name
        }
    )



class RequestUserView(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = UserAuth.objects.none()
    serializer_class = RequestUserSerializer

    def get_queryset(self):
        authenticated_user = self.request.user
        queryset = UserAuth.objects.filter(username=authenticated_user)
        return queryset
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserView(viewsets.ModelViewSet):
    queryset = UserAuth.objects.none()
    def get_queryset(self):
        authenticated_user = self.request.user
        queryset = UserAuth.objects.exclude(username=authenticated_user.username)
        return queryset
    
    serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MessageView(viewsets.ModelViewSet):
    # queryset = Message.objects.all()
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class RoomsView(viewsets.ModelViewSet):
    queryset = channelLayers.objects.none()
    def get_queryset(self):
        authenticated_user = self.request.user
        queryset = channelLayers.objects.filter(Q(client1=authenticated_user) | Q(client2=authenticated_user))
        return queryset
    serializer_class = RoomsSerializer


def user_messages(request, s_name, r_name):
    sender_name = UserAuth.objects.get(username = s_name)
    receiver_name = UserAuth.objects.get(username = r_name)
    user_messages = Message.objects.filter(sender = sender_name, Receiver=receiver_name )
    if request.method == 'GET':
        serializer = MessageSerializer(user_messages, many=True )
        return JsonResponse(serializer.data, safe=False )


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
