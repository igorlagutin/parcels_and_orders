from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.utils import timezone
from inbox.models import Deliver, Ticket, Content


class InboxModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        deliver = Deliver.objects.create(name='Nova Post')
        content = Content.objects.create(name='Parcel')
        Ticket.objects.create(
            deliver=deliver,
            serial="555555555555555",
            quantity_of_places=3,
            sender="TestSender",
            content=content
        )

    @classmethod
    def tearDownClass(cls):
        Ticket.objects.all().delete()
        Deliver.objects.all().delete()
        Content.objects.all().delete()

    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='12test12',
            email='test@example.com'
        )
        self.user.save()

        self.request = RequestFactory()
        self.request.user = self.user

    def tearDown(self):
        self.user.delete()

    def test_deliver_created(self):
        self.assertEqual(Deliver.objects.last().name, 'Nova Post')

    def test_content_created(self):
        self.assertEqual(Content.objects.last().name, 'Parcel')

    def test_created_ticket(self):
        ticket = Ticket.objects.last()
        self.assertEqual(ticket.serial, "555555555555555")
        self.assertEqual(ticket.deliver.name, "Nova Post")
        self.assertEqual(ticket.quantity_of_places, 3)
        self.assertEqual(ticket.sender, "TestSender")
        self.assertEqual(ticket.content.name, "Parcel")
        self.assertEqual(ticket.is_received, False)
        self.assertEqual(ticket.created_on.date(), timezone.now().date())
        self.assertEqual(ticket.modified_on.date(), timezone.now().date())
