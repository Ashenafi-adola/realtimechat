from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from . models import Message, CustomUser
import json
from django.utils import timezone
from asgiref.sync import async_to_sync

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        friend = self.scope['url_route']['kwargs']['friend']
        urs = [user.username, friend]
        urs.sort()
        self.room_group_name = f'chat_{urs[0]}_{urs[1]}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        reciever = text_data_json['reciever']
        sender = text_data_json['sender']
        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'reciever': reciever,
                'timestamp': str(self.get_current_timestamp()),
            }
        )
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        reciever = event['reciever']
        timestamp = event['timestamp']
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'sender': sender,
            'reciever': reciever,
            'timestamp':timestamp,
        }))

    @database_sync_to_async
    def save_message(self, message):
        sen = CustomUser.objects.get(id=self.scope['user'].id)
        rec = CustomUser.objects.get(username=self.scope['url_route']['kwargs']['friend'])
        Message.objects.create(sender=sen, reciever=rec, body=message)

    def  get_current_timestamp(self):
        return timezone.now()