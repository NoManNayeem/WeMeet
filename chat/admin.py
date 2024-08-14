from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'meeting', 'message', 'timestamp')
    search_fields = ('user__username', 'meeting__title', 'message')
    list_filter = ('timestamp',)
