from inbox.models import Ticket
from django.shortcuts import get_object_or_404


class TicketRepozitory:

    def __init__(self, request):
        self.request = request

    @staticmethod
    def get_ticket_list():
        return Ticket.objects.order_by('deliver', 'created_on')

    @staticmethod
    def get_ticket_by_pk(pk):
        return get_object_or_404(Ticket, pk=pk)