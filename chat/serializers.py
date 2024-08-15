from rest_framework import serializers
from .models import ChatGroup, ChatMessage, MeetingChatMessage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ChatGroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ChatGroup
        fields = ['id', 'name', 'members', 'created_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    group = ChatGroupSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'recipient', 'group', 'message', 'timestamp']
        read_only_fields = ['sender', 'timestamp']

class MeetingChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    meeting = serializers.StringRelatedField()  # or use a custom MeetingSerializer if more details are needed

    class Meta:
        model = MeetingChatMessage
        fields = ['id', 'meeting', 'sender', 'message', 'timestamp']
        read_only_fields = ['sender', 'timestamp']

