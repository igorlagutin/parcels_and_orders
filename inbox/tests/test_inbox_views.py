from django.contrib.auth.models import Permission, User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from inbox.models import Deliver, Ticket, Content



class InboxViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Deliver.objects.create(name='Nova Post')
        Content.objects.create(name='Parcel')

    @classmethod
    def tearDownClass(cls):
        Deliver.objects.all().delete()
        Content.objects.all().delete()


    def setUp(self):
        self.user_with_manager_perm = User.objects.create_user(
            username='user_with_manager_perm',
            password='12test12',
            email='user_with_manager_perm@example.com'
        )
        self.user_with_manager_perm.user_permissions.add(
            Permission.objects.get(codename__contains="manager")
        )
        self.user_with_manager_perm.save()


        self.user_with_manager_perm_not_creator = User.objects.create_user(
            username='user_with_manager_perm_not_creator',
            password='12test12',
            email='test@example.com'
        )
        self.user_with_manager_perm_not_creator.user_permissions.add(
            Permission.objects.get(codename__contains="manager")
        )
        self.user_with_manager_perm_not_creator.save()


        self.user_with_no_manager_perm = User.objects.create_user(
            username='user_with_no_manager_perm',
            password='12test12',
            email='test@example.com'
        )
        self.user_with_no_manager_perm.save()



        self.request = RequestFactory()
        self.request.user = self.user_with_manager_perm


        self.undebited_ticket = Ticket.objects.create(
            deliver=Deliver.objects.last(),
            serial="555555555555555",
            quantity_of_places=3,
            sender="TestSender",
            content=Content.objects.last(),
            creator=self.user_with_manager_perm
        )



        self.debited_ticket = Ticket.objects.create(
            deliver=Deliver.objects.last(),
            serial="555555555555554",
            quantity_of_places=3,
            sender="TestSender",
            content=Content.objects.last(),
            is_received = True,
            creator=self.user_with_manager_perm,
            debit_sign=self.user_with_manager_perm
        )

    def tearDown(self):
        Ticket.objects.all().delete()
        User.objects.all().delete()



    def test_unauthentificated_index(self):
        response = self.client.get(reverse('inbox'))
        self.assertRedirects(
            response,
            '/accounts/login/?next={}'.format(reverse('inbox')),
            status_code=302,
            target_status_code=200
        )


    def test_authentificated_index(self):
        self.client.login(username='user_with_manager_perm', password='12test12')
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)


    def test_unauthentificated_create(self):
        target_url = reverse('inbox_create')
        response = self.client.get(target_url)
        self.assertRedirects(
            response,
            '/accounts/login/?next={}'.format(target_url),
            status_code=302,
            target_status_code=200
        )

    def test_authentificated_create_with_no_prms(self):
        self.client.login(username='user_with_no_manager_perm', password='12test12')
        response = self.client.get(reverse('inbox_create'))
        self.assertEqual(response.status_code, 403)

    def test_authentificated_create_with_perm(self):
        self.client.login(username='user_with_manager_perm', password='12test12')
        response = self.client.get(reverse('inbox_create'))
        self.assertEqual(response.status_code, 200)


    def test_unauthentificated_detail(self):
        ticket_id = Ticket.objects.last().pk
        target_url = reverse('inbox_detail', kwargs={"pk": ticket_id})
        response = self.client.get(target_url)
        self.assertRedirects(
            response,
            '/accounts/login/?next={}'.format(target_url),
            status_code=302,
            target_status_code=200
        )

    def test_authentificated_detail(self):
        ticket_id = Ticket.objects.last().pk
        target_url = reverse('inbox_detail', kwargs={"pk": ticket_id})
        self.client.login(username='user_with_manager_perm', password='12test12')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)

    def test_unauthentificated_edit(self):
        ticket_id = Ticket.objects.last().pk
        targrt_url = reverse('inbox_edit', kwargs={"pk": ticket_id})
        response = self.client.get(targrt_url)
        self.assertRedirects(
            response,
            '/accounts/login/?next={}'.format(targrt_url),
            status_code=302,
            target_status_code=200
        )

    def test_authentificated_edit_by_author(self):
        ticket_id = Ticket.objects.get(serial="555555555555555").pk
        target_url = reverse('inbox_edit', kwargs={"pk": ticket_id})
        self.client.login(username='user_with_manager_perm', password='12test12')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)

    def test_authentificated_edit_by_non_author(self):
        ticket_id = Ticket.objects.get(serial="555555555555555").pk
        target_url = reverse('inbox_edit', kwargs={"pk": ticket_id})
        self.client.login(username='user_with_manager_perm_not_creator', password='12test12')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 404)


    def test_authentificated_edit_of_debited(self):
        ticket_id = Ticket.objects.filter(serial="555555555555554").last().pk
        target_url = reverse('inbox_edit', kwargs={"pk": ticket_id})
        self.client.login(username='user_with_manager_perm', password='12test12')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 404)