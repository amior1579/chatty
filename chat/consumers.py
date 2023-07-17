# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

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
        message = text_data_json["messageee"]
        user_sender = str(text_data_json["user_sender"])
        user_receiver = str(text_data_json["user_receiver"])
        print(user_sender)
        print(text_data_json)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message", 
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
        # print(event)
        message = event["message"]


        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message
        }))



@database_sync_to_async
def Save_Messages(message,user_sender, user_receiver, user):
    # print('database',user)
    # print('database',user_sender)
    senderr = UserAuth.objects.get(username = user_sender)
    receiverr = UserAuth.objects.get(username = user_receiver)
    return Message.objects.create(content=message, sender=senderr , Receiver=receiverr)