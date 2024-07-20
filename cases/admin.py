from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from cases.models import Case


class CaseAdmin(admin.ModelAdmin):
    list_display = (
        'case_number', 'amount', 'created_at', 'deadline', 'description'
    )
    list_filter = ('created_at', 'amount')
    search_fields = ('case_number', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('case_number', 'amount', 'description')
        }),
        ('Dates', {
            'fields': ('created_at', 'deadline'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being created
            obj.deadline = timezone.now() + timedelta(days=7)
        super().save_model(request, obj, form, change)


admin.site.register(Case, CaseAdmin)
