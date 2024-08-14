from rest_framework import serializers
from .models import Meeting

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'host', 'title', 'meeting_url', 'created_at']
        read_only_fields = ['host', 'created_at']
