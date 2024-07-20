from django.contrib import admin
from .models import Member


class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'phone_number',
        'member_number', 'national_id_number', 'account_balance'
    )
    list_filter = ('account_balance',)
    search_fields = (
        'first_name', 'last_name', 'member_number', 'national_id_number'
    )
    ordering = ('last_name', 'first_name')
    fieldsets = (
        (None, {
            'fields': (
                'first_name', 'last_name', 'phone_number',
                'member_number', 'national_id_number', 'account_balance'
            )
        }),
    )


admin.site.register(Member, MemberAdmin)
