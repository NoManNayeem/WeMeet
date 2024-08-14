from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Meeting
from .serializers import MeetingSerializer

class MeetingCreateView(generics.CreateAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

class MeetingListView(generics.ListAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Meeting.objects.filter(host=self.request.user)
