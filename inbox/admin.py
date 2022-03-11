from django.contrib import admin
from inbox.models import Ticket, Content, Deliver


admin.site.register(Ticket)
admin.site.register(Content)
admin.site.register(Deliver)
