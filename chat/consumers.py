import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from .models import ChatMessage, Meeting
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.meeting_id = self.scope['url_route']['kwargs']['meeting_id']
        self.room_group_name = f'chat_{self.meeting_id}'

        # Check if the meeting exists
        try:
            self.meeting = await database_sync_to_async(Meeting.objects.get)(id=self.meeting_id)
        except Meeting.DoesNotExist:
            # If the meeting does not exist, reject the WebSocket connection
            await self.close()
            return

        # Set the user status to active
        self.scope['user'].profile.status = True
        await database_sync_to_async(self.scope['user'].profile.save)()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Notify others that a user has joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.scope["user"].username} has joined the chat.',
            }
        )

    async def disconnect(self, close_code):
        # Set the user status to inactive
        self.scope['user'].profile.status = False
        await database_sync_to_async(self.scope['user'].profile.save)()

        # Notify others that a user has left
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.scope["user"].username} has left the chat.',
            }
        )

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        try:
            # Save the message to the database
            await database_sync_to_async(ChatMessage.objects.create)(
                meeting=self.meeting,
                user=self.scope["user"],
                message=message
            )

            # Broadcast the message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                }
            )
        except ObjectDoesNotExist as e:
            logger.error(f"Object does not exist: {e}")
            await self.send(text_data=json.dumps({'error': 'Meeting or User does not exist'}))
        except Exception as e:
            logger.error(f"Error saving chat message: {e}")
            await self.send(text_data=json.dumps({'error': 'Error saving message'}))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
