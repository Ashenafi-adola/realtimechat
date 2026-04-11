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
        if text_data_json['command'] == 'send':
            message = text_data_json['message']
            reciever = text_data_json['reciever']
            sender = text_data_json['sender']
            id = await self.save_message(message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender,
                    'reciever': reciever,
                    'timestamp': str(self.get_current_timestamp()),
                    'id': id
                }
            )
        else:
            id = text_data_json['id']
            print(id)
            await self.delete_message(id)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'delete_chat',
                    'id': id,
                }
            )
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        reciever = event['reciever']
        timestamp = event['timestamp']
        id = event['id']
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'sender': sender,
            'reciever': reciever,
            'timestamp':timestamp,
            'id': id
        }))
    async def delete_chat(self, event):
        id = event['id']
        await self.send(text_data=json.dumps({
            'type': 'delete',
            'id' : id
        }))

    @database_sync_to_async
    def save_message(self, message):
        sen = CustomUser.objects.get(id=self.scope['user'].id)
        rec = CustomUser.objects.get(username=self.scope['url_route']['kwargs']['friend'])
        mes = Message(sender=sen, reciever=rec, body=message)
        mes.save()
        return mes.id

    @database_sync_to_async
    def delete_message(self, id):
        message = Message.objects.get(id=id)
        message.delete()

    def  get_current_timestamp(self):
        return timezone.now()