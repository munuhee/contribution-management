from django.contrib import admin
from .models import Invoice, Transaction, UnmatchedTransactions


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number', 'issue_date', 'due_date', 'amount', 'is_settled'
    )
    list_filter = ('issue_date', 'due_date', 'is_settled')
    search_fields = ('invoice_number', 'description')
    ordering = ('-issue_date',)
    date_hierarchy = 'issue_date'
    fieldsets = (
        (None, {
            'fields': ('invoice_number', 'amount', 'description', 'is_settled')
        }),
        ('Date Information', {
            'fields': ('issue_date', 'due_date'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('issue_date',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'member', 'trans_id', 'reference', 'transaction_type',
        'phone_number', 'amount', 'date', 'invoice'
    )
    list_filter = ('date', 'member', 'transaction_type', 'invoice')
    search_fields = ('trans_id', 'reference', 'phone_number', 'amount')
    ordering = ('-date',)
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': (
                'member', 'trans_id', 'reference', 'transaction_type',
                'phone_number', 'amount', 'invoice'
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


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(UnmatchedTransactions, UnmatchedTransactionsAdmin)
