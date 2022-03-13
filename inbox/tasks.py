from celery import shared_task
from django.utils import timezone
import telegram
from inbox.const import PARCEL_ARRIVED_STATUS_LIST,DELIVER_REFRESH_STATUS_LIST,\
    SHIPMENT_RECEIVED_WAIT_SMS_STATUS, SHIPMENT_RECEIVED_MONEY_IS_READY_STATUS, \
    PARCEL_ISSUED_STATUS_STATUS
from inbox.repozitory import TicketDBRepozitory
from parcels_and_orders.env import BOT_TOKEN, CHAT_ID

def send_to_telegram(chat_id: str, message: str) -> None:
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode=telegram.ParseMode.MARKDOWN)
    return None





@shared_task()
def refresh_all_tickets_status() -> None :
    repozitory = TicketDBRepozitory()
    all_tickets = repozitory.get_ticket_list()
    tickets = all_tickets.filter(
        is_received=False,
        deliver__name__in=DELIVER_REFRESH_STATUS_LIST)
    for ticket in tickets:
        old_status = ticket.delivery_status
        refresh_result = TicketDBRepozitory().refresh_ticket_status_from_api(ticket.id)

        #send messages to telegramm accordin to status changes
        if old_status != refresh_result["delivery_status"]:
            if refresh_result["delivery_status"] in PARCEL_ARRIVED_STATUS_LIST:
                message = "№ *%s* \n\rот _%s_ \n\rприбыл на *%s* \n\r%s" \
                          % (ticket.serial,
                             ticket.sender,
                             ticket.deliver.name,
                             refresh_result["WarehouseRecipient"]
                             )
                send_to_telegram(CHAT_ID, message)

            elif (refresh_result["delivery_status"] == SHIPMENT_RECEIVED_WAIT_SMS_STATUS):
                message = "№ *%s* \n\rот _%s_ \n\rПосылка забрана, можно забирать наложенный: *%s*" % (
                    ticket.serial,
                    ticket.sender,
                    ticket.money
                )
                send_to_telegram(CHAT_ID, message)

            elif (refresh_result["delivery_status"] == SHIPMENT_RECEIVED_MONEY_IS_READY_STATUS):
                message = "№ *%s* \n\rот _%s_ \n\rНаложенный выдан, сумма: *%s*" \
                          % (ticket.serial,
                             ticket.sender,
                             ticket.money
                             )
                send_to_telegram(CHAT_ID, message)

            elif refresh_result["delivery_status"] in PARCEL_ISSUED_STATUS_STATUS:
                ticket.notes = "{} \n\r Забрано: {}".format(
                    ticket.notes,
                    timezone.now().strftime("%d/%m/%Y %H:%M:%S"))
                ticket.save()