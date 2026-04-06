from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        friend = self.scope['url_route']['kwargs']['friend']
        urs = [user.username, friend]
        urs.sort()
        self.room_group_name = f'chat_{urs[0]}_{urs[1]}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()


    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        reciever = text_data_json['reciever']
        sender = text_data_json['sender']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'reciever': reciever
            }
        )
    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        reciever = event['reciever']
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'sender': sender,
            'reciever': reciever,
        }))