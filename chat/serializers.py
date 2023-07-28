from rest_framework import serializers
from .models import *
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class UserSerializer(serializers.HyperlinkedModelSerializer):
class RequestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuth
        fields = '__all__'

# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuth
        # fields = '__all__'
        fields = ('id','username','email','url')


# class MessageSerializer(serializers.HyperlinkedModelSerializer):
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        # fields = ('id','username','email','url')


# class MessageSerializer(serializers.HyperlinkedModelSerializer):
class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = channelLayers
        fields = '__all__'
        # fields = ('id','username','email','url')
