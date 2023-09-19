from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Post

class NotificationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.roomGroupName = "notification"
        await self.channel_layer.group_add(
            self.roomGroupName ,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self , close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName ,
            self.channel_name
        )
    async def receive(self, text_data):
        pass

    async def sendNotification(self , event) :
        message = event['message']
        post_author = event['post_author'] 
        await self.send(text_data = json.dumps({'message' : message ,'post_author' : post_author}))