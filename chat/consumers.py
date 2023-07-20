# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import *



class ChatConsumer(AsyncWebsocketConsumer):
    # @database_sync_to_async
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.user_request = self.scope['user']
        self.room_group_name = "chat_%s" % self.room_name

        # print('scooooop ',self.scope["subprotocols"])
        # {
            # 'type': 'websocket', 
            #  'path': '/ws/chat/amir_to_amir/', 
            #  'raw_path': b'/ws/chat/amir_to_amir/', 
            #  'headers': [
            #      (b'host', b'127.0.0.1:8000'), 
            #      (b'connection', b'Upgrade'), 
            #      (b'pragma', b'no-cache'), 
            #      (b'cache-control', b'no-cache'), 
            #      (b'user-agent', b'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'), 
            #      (b'upgrade', b'websocket'), 
            #      (b'origin', b'http://127.0.0.1:8000'), 
            #      (b'sec-websocket-version', b'13'), 
            #      (b'accept-encoding', b'gzip, deflate, br'), 
            #      (b'accept-language', b'en-GB,en;q=0.9,fa-IR;q=0.8,fa;q=0.7,en-US;q=0.6'), 
            #      (b'cookie', b'csrftoken=bcU7FGTK2QHFPJsElg2SIYyR5mKFDz5b; sessionid=aoxh64ac2v7l9zo4kj7soljupq5qwkwk; tabstyle=html-tab'), 
            #      (b'sec-websocket-key', b'dqgbKUD9zBPYviLK7XqgJA=='), 
            #      (b'sec-websocket-extensions', b'permessage-deflate; client_max_window_bits')], 
            #  'query_string': b'', 
            #  'client': ['127.0.0.1', 53854], 
            #  'server': ['127.0.0.1', 8000], 
            #  'subprotocols': [], 
            #  'asgi': {'version': '3.0'}, 
            #  'cookies': {'csrftoken': 'bcU7FGTK2QHFPJsElg2SIYyR5mKFDz5b', 'sessionid': 'aoxh64ac2v7l9zo4kj7soljupq5qwkwk', 'tabstyle': 'html-tab'}, 
            #  'session': <django.utils.functional.LazyObject object at 0x104a76950>, 
            #  'user': <channels.auth.UserLazyObject object at 0x104af77d0>, 
            #  'path_remaining': '', 
            #  'url_route': {'args': (), 'kwargs': {'room_name': 'amir_to_amir'}}
        #  }

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('text_data_jsonnnn', text_data_json)
        message = text_data_json["messageee"]
        user_sender = str(text_data_json["user_sender"])
        user_receiver = str(text_data_json["user_receiver"])
        # print(user_sender)
        # print(text_data_json)

        self.Layers = await Channel_Layers(self.room_group_name,self.user_request)
        print(self.Layers)
        if self.Layers == False:
            await Save_layer(
                self.room_group_name,  
                self.user_request  
            )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message", 
                "username": self.scope["user"].username,
                "message": message
            }
        )

        await Save_Messages(
            message,
            user_sender,
            user_receiver,
            self.scope['user']
        )

    # Receive message from room group
    async def chat_message(self, event):
        # print('eventttt',event)
        message = event["message"]
        username = event["username"]


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))



@database_sync_to_async
def Save_Messages(message,user_sender, user_receiver, user):
    # print('database',user)
    # print('database',user_sender)
    senderr = UserAuth.objects.get(username = user_sender)
    receiverr = UserAuth.objects.get(username = user_receiver)
    return Message.objects.create(content=message, sender=senderr , Receiver=receiverr)


@database_sync_to_async
def Save_layer(room_group_name,user_request):
    # print('database',user)
    # print('database',user_sender)
    # senderr = UserAuth.objects.get(username = user_sender)
    # receiverr = UserAuth.objects.get(username = user_receiver)
    return channelLayers.objects.create(room_name=room_group_name, client1=user_request)


@database_sync_to_async
def Channel_Layers(room_group_name,user_request):
    return channelLayers.objects.filter(room_name=room_group_name, client1=user_request).exists()
