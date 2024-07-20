from django.contrib import admin
from .models import Transaction, UnmatchedTransactions


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'member', 'trans_id', 'reference', 'phone_number', 'amount', 'date'
    )
    list_filter = ('date', 'member')
    search_fields = ('trans_id', 'reference', 'phone_number', 'amount')
    ordering = ('-date',)
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': (
                'member', 'trans_id', 'reference', 'phone_number', 'amount'
            )
        }),
        ('Date Information', {
            'fields': ('date',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('date',)


class UnmatchedTransactionsAdmin(admin.ModelAdmin):
    list_display = ('trans_id', 'reference', 'phone_number', 'amount', 'date')
    list_filter = ('date',)
    search_fields = ('trans_id', 'reference', 'phone_number', 'amount')
    ordering = ('-date',)
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('trans_id', 'reference', 'phone_number', 'amount')
        }),
        ('Date Information', {
            'fields': ('date',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('date',)


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(UnmatchedTransactions, UnmatchedTransactionsAdmin)
