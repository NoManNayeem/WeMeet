from django.urls import path
from .views import ChatMessageCreateView, ChatMessageListView

urlpatterns = [
    path('send/', ChatMessageCreateView.as_view(), name='chat-send'),
    path('<int:meeting_id>/', ChatMessageListView.as_view(), name='chat-list'),
]
