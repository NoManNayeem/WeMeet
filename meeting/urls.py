from django.urls import path
from .views import MeetingCreateView, MeetingListView

urlpatterns = [
    path('create/', MeetingCreateView.as_view(), name='meeting-create'),
    path('', MeetingListView.as_view(), name='meeting-list'),
]
