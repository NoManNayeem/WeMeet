from django.contrib import admin
from .models import ChatGroup, ChatMessage, MeetingChatMessage

@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    filter_horizontal = ('members',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'group', 'message', 'timestamp')
    list_filter = ('timestamp', 'group')
    search_fields = ('sender__username', 'recipient__username', 'group__name', 'message')

@admin.register(MeetingChatMessage)
class MeetingChatMessageAdmin(admin.ModelAdmin):
    list_display = ('meeting', 'sender', 'message', 'timestamp')
    list_filter = ('timestamp', 'meeting')
    search_fields = ('sender__username', 'meeting__id', 'message')
