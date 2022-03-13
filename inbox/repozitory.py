from inbox.models import Ticket
from django.shortcuts import get_object_or_404
from inbox.api_utils import ApiTicketStatusUtils


class TicketDBRepozitory:

    @staticmethod
    def get_ticket_list():
        return Ticket.objects.order_by('-deliver', '-created_on')

    @staticmethod
    def get_ticket_by_pk(pk):
        return get_object_or_404(Ticket, pk=pk)

    def refresh_ticket_status_from_api(self, ticket_id: int) -> dict:
        ticket = self.get_ticket_by_pk(ticket_id)
        raw_status = ApiTicketStatusUtils(
            ticket.serial,
            ticket.deliver.name).get_ticket_deliver_status()

        ticket.delivery_status = raw_status.get('Status')
        ticket.delivery_destination = raw_status.get('WarehouseRecipient')
        ticket.save()
        return {
            'delivery_status': ticket.delivery_status,
            'delivery_destination': ticket.delivery_destination
        }

    def get_ticket_status_from_api(self, pk: int) -> dict:
        ticket = self.get_ticket_by_pk(pk)
        return ApiTicketStatusUtils(
            ticket.serial,
            ticket.deliver.name).get_ticket_deliver_status()