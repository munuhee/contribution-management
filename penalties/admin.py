from django.contrib import admin
from .models import Penalty


class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('member', 'invoice', 'date', 'amount', 'is_paid')
    list_filter = ('is_paid', 'date')
    search_fields = (
        'member__first_name', 'member__last_name',
        'invoice__invoice_number', 'amount'
    )
    ordering = ('-date',)
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('member', 'invoice', 'amount', 'is_paid')
        }),
        ('Date Information', {
            'fields': ('date',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('date',)


admin.site.register(Penalty, PenaltyAdmin)
