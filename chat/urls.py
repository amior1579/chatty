from django.urls import path, include
from . import views
# from rest_framework import routers
from .views import *

from rest_framework import routers
router = routers.DefaultRouter()
router.register('Request User', views.RequestUserView, basename='Request User')
router.register('Users', views.UserView)
router.register('Message', views.MessageView)



urlpatterns = [
    path('', views.index, name='index'),
    path('login_page', views.login_page, name='login_page'),
    path('register_page', views.register_page, name='register_page'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('user_registration', views.user_registration, name='user_registration'),
    path('user_login', views.user_login, name='user_login'),
    
    path("<str:room_name>/", views.room, name="room"),

    path('apis/chatapi', include(router.urls)),
    path('apis/chatapiMessage/<str:s_name>/to/<str:r_name>', views.user_messages, name='user_messages'),

]