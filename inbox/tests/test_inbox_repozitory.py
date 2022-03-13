from unittest import mock
from django.test import TestCase
from inbox.models import Ticket, Deliver, Content
from inbox.repozitory import TicketDBRepozitory
from inbox.api_utils import ApiTicketStatusUtils


class IndexRepozitoryTest(TestCase):

    def setUp(self):
        self.get_ticket_deliver_status_mock_object = {
            'CityRecipient': 'testCity',
            'WarehouseRecipient': 'testRecipient',
            'ScheduledDeliveryDate': 'testDate',
            'Status': 'testStatus'
        }
        self.patcher = mock.patch.object(
            ApiTicketStatusUtils,
            'get_ticket_deliver_status',
            return_value=self.get_ticket_deliver_status_mock_object)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    @classmethod
    def setUpClass(cls):
        deliver = Deliver.objects.create(name="Nova Post")
        content = Content.objects.create(name="Parcel")
        for i in range(5):
            Ticket.objects.create(
                deliver=deliver,
                serial=i,
                sender="lorem {}".format(i),
                content=content
            )

    @classmethod
    def tearDownClass(cls):
        Ticket.objects.all().delete()
        Deliver.objects.all().delete()
        Content.objects.all().delete()

    def test_get_ticket_list_return_ticket_list(self):
        self.assertEqual(TicketDBRepozitory.get_ticket_list().count(), 5)

    def test_get_ticket_by_pk_return_ticket_if_exist(self):
        ticket_from_db = Ticket.objects.last()
        ticket_from_repo = TicketDBRepozitory.get_ticket_by_pk(ticket_from_db.pk)
        self.assertEqual(ticket_from_db, ticket_from_repo)

    def test_refresh_ticket_status_from_api(self):
        ticket = Ticket.objects.last()
        TicketDBRepozitory.refresh_ticket_status_from_api(ticket.pk)
        ticket_after_refresh = Ticket.objects.get(pk=ticket.pk)
        self.assertEqual(ticket_after_refresh.delivery_status, "testStatus")
        self.assertEqual(ticket_after_refresh.delivery_destination, "testRecipient")

    def test_get_ticket_status_from_api(self):
        ticket = Ticket.objects.last()
        response = TicketDBRepozitory.get_ticket_status_from_api(ticket.pk)
        for key, value in self.get_ticket_deliver_status_mock_object.items():
            self.assertEqual(response[key], value)
