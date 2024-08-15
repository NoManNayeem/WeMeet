import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatMessage, ChatGroup, MeetingChatMessage
from meeting.models import Meeting
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Set the user status to active
        self.scope['user'].profile.status = True
        await database_sync_to_async(self.scope['user'].profile.save)()

        await self.accept()

    async def disconnect(self, close_code):
        # Set the user status to inactive
        self.scope['user'].profile.status = False
        await database_sync_to_async(self.scope['user'].profile.save)()

        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room_type = text_data_json.get('room_type')  # either 'private', 'group', or 'meeting'

        if room_type == 'private':
            recipient_id = text_data_json['recipient_id']
            recipient = await database_sync_to_async(User.objects.get)(id=recipient_id)
            await database_sync_to_async(ChatMessage.objects.create)(
                sender=self.scope['user'],
                recipient=recipient,
                message=message
            )
        elif room_type == 'group':
            group_id = text_data_json['group_id']
            group = await database_sync_to_async(ChatGroup.objects.get)(id=group_id)
            await database_sync_to_async(ChatMessage.objects.create)(
                sender=self.scope['user'],
                group=group,
                message=message
            )
        elif room_type == 'meeting':
            meeting_id = text_data_json['meeting_id']
            meeting = await database_sync_to_async(Meeting.objects.get)(id=meeting_id)
            await database_sync_to_async(MeetingChatMessage.objects.create)(
                sender=self.scope['user'],
                meeting=meeting,
                message=message
            )

        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope['user'].username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
