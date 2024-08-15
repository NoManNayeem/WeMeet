from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import ChatGroup, ChatMessage, MeetingChatMessage
from .serializers import ChatGroupSerializer, ChatMessageSerializer, MeetingChatMessageSerializer
from meeting.models import Meeting

class ChatGroupCreateView(generics.CreateAPIView):
    serializer_class = ChatGroupSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        group = serializer.save()
        group.members.add(self.request.user)  # Add the creator to the group automatically

class ChatGroupListView(generics.ListAPIView):
    serializer_class = ChatGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatGroup.objects.filter(members=self.request.user)

class ChatMessageCreateView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        recipient_id = self.request.data.get('recipient_id')
        group_id = self.request.data.get('group_id')

        if recipient_id:
            recipient = User.objects.get(id=recipient_id)
            serializer.save(sender=self.request.user, recipient=recipient)
        elif group_id:
            group = ChatGroup.objects.get(id=group_id)
            serializer.save(sender=self.request.user, group=group)
        else:
            raise serializers.ValidationError("Must provide either recipient_id or group_id")

class ChatMessageListView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        recipient_id = self.kwargs.get('recipient_id')
        group_id = self.kwargs.get('group_id')

        if recipient_id:
            return ChatMessage.objects.filter(
                sender=self.request.user,
                recipient_id=recipient_id
            ).order_by('timestamp')
        elif group_id:
            return ChatMessage.objects.filter(
                group_id=group_id
            ).order_by('timestamp')
        else:
            return ChatMessage.objects.none()

class MeetingChatMessageCreateView(generics.CreateAPIView):
    serializer_class = MeetingChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        meeting_id = self.request.data.get('meeting_id')
        meeting = Meeting.objects.get(id=meeting_id)
        serializer.save(sender=self.request.user, meeting=meeting)

class MeetingChatMessageListView(generics.ListAPIView):
    serializer_class = MeetingChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        meeting_id = self.kwargs['meeting_id']
        return MeetingChatMessage.objects.filter(meeting_id=meeting_id).order_by('timestamp')
