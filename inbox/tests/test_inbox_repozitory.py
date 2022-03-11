from django.test import TestCase
from inbox.models import Ticket, Deliver, Content
from inbox.repozitory import TicketRepozitory


class IndexRepozitoryTest(TestCase):

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
        self.assertEqual(TicketRepozitory.get_ticket_list().count(), 5)

    def test_get_ticket_by_pk_return_ticket_if_exist(self):
        ticket_from_db = Ticket.objects.get(pk=3)
        ticket_from_repo = TicketRepozitory.get_ticket_by_pk(3)
        self.assertEqual(ticket_from_db, ticket_from_repo)
