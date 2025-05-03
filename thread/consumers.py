import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Thread, Comment, Like


class ThreadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.thread_group_name = f'thread_{self.thread_id}'

        # Join thread group
        await self.channel_layer.group_add(
            self.thread_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave thread group
        await self.channel_layer.group_discard(
            self.thread_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        pass

    # Receive message from thread group
    async def thread_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['content'], ensure_ascii=False))

    # Receive message for comment update
    async def comment_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['content'], ensure_ascii=False))

    # Receive message for like update
    async def like_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['content'], ensure_ascii=False))


class UserNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_group_name = f'user_{self.user_id}'

        # Join user group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave user group
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        pass

    # Receive message from user group
    async def notification_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['content'], ensure_ascii=False)) 