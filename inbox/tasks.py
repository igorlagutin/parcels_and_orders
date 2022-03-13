from celery import shared_task
from inbox.const import DELIVER_REFRESH_STATUS_LIST
from inbox.repozitory import TicketDBRepozitory


@shared_task()
def refresh_all_tickets_status() -> None :
    repozitory = TicketDBRepozitory()
    all_tickets = repozitory.get_ticket_list()
    tickets = all_tickets.filter(
        is_received=False,
        deliver__name__in=DELIVER_REFRESH_STATUS_LIST)
    for ticket in tickets:
        TicketDBRepozitory().refresh_ticket_status_from_api(ticket.id)
