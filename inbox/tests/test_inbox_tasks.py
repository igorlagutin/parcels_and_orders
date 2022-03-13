from unittest import mock
from django.test import TestCase
from inbox.models import Ticket, Deliver, Content
from inbox.tasks import refresh_all_tickets_status
from inbox.api_utils import ApiTicketStatusUtils


class IndexTaskTest(TestCase):

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
        cls.nova_post_deliver = Deliver.objects.create(name="Новая Почта")
        cls.autolux_deliver = Deliver.objects.create(name="Автолюкс")
        cls.other_deliver = Deliver.objects.create(name="Другой перевозчик")
        content = Content.objects.create(name="Parcel")
        deliver_list = [cls.nova_post_deliver, cls.autolux_deliver, cls.other_deliver]
        for deliver, i in zip(deliver_list, range(len(deliver_list))):
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

    def test_refresh_all_tickets_status(self):
        refresh_all_tickets_status()
        tickets_should_be_updated = Ticket.objects.filter(
            deliver__in=[self.nova_post_deliver, self.autolux_deliver])
        tickets_should_not_be_updated = Ticket.objects.filter(
            deliver=self.other_deliver)

        for ticket in tickets_should_be_updated:
            self.assertEqual(ticket.delivery_status, "testStatus")
            self.assertEqual(ticket.delivery_destination, "testRecipient")
        for ticket in tickets_should_not_be_updated:
            self.assertEqual(ticket.delivery_status, None)
            self.assertEqual(ticket.delivery_destination, None)