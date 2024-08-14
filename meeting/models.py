from django.db import models
from django.contrib.auth.models import User

class Meeting(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_meetings')
    title = models.CharField(max_length=255)
    meeting_url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
