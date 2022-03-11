from inbox.models import Ticket




class TicketRepozitory:

    def __init__(self, request):
        self.request = request

    def get_ticket_list(self):
        return Ticket.objects.all()