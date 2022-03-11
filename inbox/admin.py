from django.contrib import admin
from inbox.models import Ticket, Content, Deliver



@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('serial', 'deliver')
    readonly_fields = (
        'created_on',
        'modified_on',
        'debit_on',
        'debit_sign_on',
        'delivery_destination',
        'delivery_status'
    )

admin.site.register(Content)
admin.site.register(Deliver)
