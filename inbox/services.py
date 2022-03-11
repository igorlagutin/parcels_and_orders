from django.utils import timezone

from inbox.repozitory import TicketRepozitory


class TicketService:
    def __init__(self, request: object):
        self.request = request

    def get_ticket(self, pk: int) -> object:
        return TicketRepozitory(self.request).get_ticket_by_pk(pk)

    def create(self, form: object) -> object:
        ticket = form.save(commit=False)
        ticket.creator = self.request.user
        form.save()
        return form

    def edit(self, form: object) -> object:
        ticket = form.save(commit=False)
        ticket.modified_by = self.request.user
        form.save()
        return form

    def debit(self, form: object) -> object:
        ticket = form.save(commit=False)
        ticket.is_received = not ticket.is_received
        ticket.modified_by = self.request.user

        if ticket.is_received:
            ticket.debit_sign = self.request.user
            ticket.debit_on = timezone.now()
        else:
            ticket.debit_sign = None
            ticket.debit_on = None
        form.save()
        return form
