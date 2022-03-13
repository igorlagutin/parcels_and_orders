from inbox.models import Ticket
from django.shortcuts import get_object_or_404
from inbox.api_utils import ApiTicketStatusUtils


class TicketDBRepozitory:

    @staticmethod
    def get_ticket_list() -> Ticket:
        return Ticket.objects.order_by('-deliver', '-created_on')

    @staticmethod
    def get_ticket_by_pk(pk) -> Ticket:
        return get_object_or_404(Ticket, pk=pk)

    @classmethod
    def refresh_ticket_status_from_api(cls, ticket_id: int) -> dict:
        ticket = cls.get_ticket_by_pk(ticket_id)
        raw_status = ApiTicketStatusUtils(
            ticket.serial,
            ticket.deliver.name).get_ticket_deliver_status()

        ticket.delivery_status = raw_status.get('Status')
        ticket.delivery_destination = raw_status.get('WarehouseRecipient')
        ticket.save()
        return {
            'Status': ticket.delivery_status,
            'WarehouseRecipient': ticket.delivery_destination}

    @classmethod
    def get_ticket_status_from_api(cls, ticket_pk: int) -> dict:
        ticket = cls.get_ticket_by_pk(ticket_pk)
        return ApiTicketStatusUtils(
            ticket.serial,
            ticket.deliver.name).get_ticket_deliver_status()
