from django.contrib import admin
from .models import SentMessage


@admin.register(SentMessage)
class SentMessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'sent_at', 'status')
    list_filter = ('status',)
    search_fields = ('message',)
    readonly_fields = ('sent_at', 'response')
    ordering = ('-sent_at',)
    date_hierarchy = 'sent_at'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If object is being edited, show response as readonly
            return self.readonly_fields + ('response',)
        return self.readonly_fields
