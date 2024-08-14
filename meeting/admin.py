from django.contrib import admin
from .models import Meeting

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'host', 'meeting_url', 'created_at')
    search_fields = ('title', 'host__username')
    list_filter = ('created_at',)
