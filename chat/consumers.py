from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': 'connection stablished successf'
        }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        self.send(text_data=text_data)