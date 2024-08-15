from django.db import models
from django.contrib.auth.models import User

class ChatGroup(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(ChatGroup, related_name='group_messages', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username}: {self.message[:50]}'


from django.db import models
from django.contrib.auth.models import User
from meeting.models import Meeting

class MeetingChatMessage(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='meeting_chat_messages')
    sender = models.ForeignKey(User, related_name='meeting_sent_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username}: {self.message[:50]} in meeting {self.meeting.id}'
