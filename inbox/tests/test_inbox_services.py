from unittest import mock
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from inbox.models import Ticket, Deliver, Content
from inbox.services import TicketService, ApiTicketService
from inbox.forms import TicketCreateEditForm, TicketViewDebitForm
from inbox.api_utils import ApiTicketStatusUtils


class IndexServiceTest(TestCase):

    @classmethod
    def setUpClass(cls):
        deliver = Deliver.objects.create(name="Nova Post")
        content = Content.objects.create(name="Parcel")
        user = User.objects.create_user(
            username='test',
            password='12test12',
            email='test@example.com'
        ).save()

        for i in range(5):
            Ticket.objects.create(
                deliver=deliver,
                serial=i,
                sender="lorem {}".format(i),
                content=content,
                creator=user
            )

    @classmethod
    def tearDownClass(cls):
        Ticket.objects.all().delete()
        Deliver.objects.all().delete()
        Content.objects.all().delete()
        User.objects.all().delete()

    def setUp(self):
        factory = RequestFactory()
        self.request = factory.get('/')
        self.request.user = User.objects.last()
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

    def test_get_ticket_returns_ticket(self):
        last_id = Ticket.objects.last().id
        ticket_from_db = Ticket.objects.get(pk=last_id)
        ticket_from_service = TicketService(self.request).get_ticket(last_id)
        self.assertEqual(ticket_from_db, ticket_from_service)

    def test_create_assigns_author(self):
        data = {
            "deliver": Deliver.objects.last().pk,
            "serial": 1112,
            "sender": "lorem 11",
            "content": Content.objects.last().pk,
            "quantity_of_places": 1,
        }
        form = TicketCreateEditForm(data, initial=data)
        updated_form = TicketService(self.request).create(form)
        ticket = updated_form.save()
        self.assertEqual(ticket.creator, self.request.user)

    def test_edit_assign_modifier(self):
        data = {
            "deliver": Deliver.objects.last().pk,
            "serial": 1115,
            "sender": "lorem 11",
            "content": Content.objects.last().pk,
            "quantity_of_places": 1,
        }
        form = TicketCreateEditForm(data, instance=Ticket.objects.last())
        updated_form = TicketService(self.request).edit(form)
        ticket = updated_form.save()
        self.assertEqual(ticket.modified_by, self.request.user)

    def test_debit_assign_debiter_and_debit_time(self):
        data = {}
        form = TicketViewDebitForm(data, instance=Ticket.objects.last())
        updated_form = TicketService(self.request).debit(form)
        ticket = updated_form.save()
        self.assertEqual(ticket.debit_sign, self.request.user)
        self.assertFalse(ticket.debit_on is None)

    def test_undebit_set_debiter_and_debit_time_to_none(self):
        data = {}
        form = TicketViewDebitForm(data, instance=Ticket.objects.last())
        TicketService(self.request).debit(form)
        updated_form = TicketService(self.request).debit(form)
        ticket = updated_form.save()
        self.assertTrue(ticket.debit_sign is None)
        self.assertTrue(ticket.debit_on is None)

    def test_get_api_status_by_serial_and_deliver_name(self):
        response = ApiTicketService.get_api_status_by_serial_and_deliver_name(11111, "test")
        for key, value in self.get_ticket_deliver_status_mock_object.items():
            self.assertEqual(response[key], value)