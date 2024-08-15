from django.urls import path
from .views import (
    ChatGroupCreateView, ChatGroupListView,
    ChatMessageCreateView, ChatMessageListView,
    MeetingChatMessageCreateView, MeetingChatMessageListView
)

urlpatterns = [
    # Chat Group URLs
    path('groups/', ChatGroupListView.as_view(), name='chat-group-list'),
    path('groups/create/', ChatGroupCreateView.as_view(), name='chat-group-create'),

    # Chat Message URLs
    path('messages/send/', ChatMessageCreateView.as_view(), name='chat-message-send'),
    path('messages/private/<int:recipient_id>/', ChatMessageListView.as_view(), name='private-message-list'),
    path('messages/group/<int:group_id>/', ChatMessageListView.as_view(), name='group-message-list'),

    # Meeting Chat Message URLs
    path('meetings/messages/send/', MeetingChatMessageCreateView.as_view(), name='meeting-chat-message-send'),
    path('meetings/<int:meeting_id>/messages/', MeetingChatMessageListView.as_view(), name='meeting-chat-message-list'),
]
