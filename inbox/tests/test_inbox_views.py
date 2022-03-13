from unittest import mock
from django.contrib.auth.models import Permission, User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from inbox.models import Deliver, Ticket, Content
from inbox.api_utils import ApiTicketStatusUtils


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
        get_ticket_deliver_status_mock_object = {
            'CityRecipient': 'testCity',
            'WarehouseRecipient': 'testRecipient',
            'ScheduledDeliveryDate': 'testDate',
            'Status': 'testStatus'
        }
        self.patcher = mock.patch.object(
            ApiTicketStatusUtils,
            'get_ticket_deliver_status',
            return_value=get_ticket_deliver_status_mock_object)
        self.mock_get_ticket_deliver_status = self.patcher.start()

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
            is_received=True,
            creator=self.user_with_manager_perm,
            debit_sign=self.user_with_manager_perm
        )

    def tearDown(self):
        Ticket.objects.all().delete()
        User.objects.all().delete()
        self.patcher.stop()

    def test_unauthenticated_index(self):
        response = self.client.get(reverse('inbox'))
        self.assertRedirects(
            response,
            '/accounts/login/?next={}'.format(reverse('inbox')),
            status_code=302,
            target_status_code=200
        )

    def test_authenticated_index(self):
        self.client.login(username='user_with_manager_perm', password='12test12')
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_create(self):
        target_url = reverse('inbox_create')
        response = self.client.get(target_url)
        self.assertRedirects(
            response,
            '/accounts/login/?next={}'.format(target_url),
            status_code=302,
            target_status_code=200
        )

    def test_authenticated_create_with_no_perms(self):
        self.client.login(username='user_with_no_manager_perm', password='12test12')
        response = self.client.get(reverse('inbox_create'))
        self.assertEqual(response.status_code, 403)

    def test_authenticated_create_with_perm(self):
        self.client.login(username='user_with_manager_perm', password='12test12')
        response = self.client.get(reverse('inbox_create'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_detail(self):
        ticket_id = self.undebited_ticket.pk
        target_url = reverse('inbox_detail', kwargs={"pk": ticket_id})
        response = self.client.get(target_url)
        self.assertRedirects(
            response,
            '/accounts/login/?next={}'.format(target_url),
            status_code=302,
            target_status_code=200
        )

    def test_authenticated_detail(self):
        ticket_id = self.undebited_ticket.pk
        target_url = reverse('inbox_detail', kwargs={"pk": ticket_id})
        self.client.login(username='user_with_manager_perm', password='12test12')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_edit(self):
        ticket_id = self.undebited_ticket.pk
        target_url = reverse('inbox_edit', kwargs={"pk": ticket_id})
        response = self.client.get(target_url)
        self.assertRedirects(
            response,
            '/accounts/login/?next={}'.format(target_url),
            status_code=302,
            target_status_code=200
        )

    def test_authenticated_edit_by_author(self):
        ticket_id = self.undebited_ticket.pk
        target_url = reverse('inbox_edit', kwargs={"pk": ticket_id})
        self.client.login(username='user_with_manager_perm', password='12test12')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_edit_by_non_author(self):
        ticket_id = self.undebited_ticket.pk
        target_url = reverse('inbox_edit', kwargs={"pk": ticket_id})
        self.client.login(username='user_with_manager_perm_not_creator', password='12test12')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 404)

    def test_authenticated_edit_of_debited(self):
        ticket_id = self.debited_ticket.pk
        target_url = reverse('inbox_edit', kwargs={"pk": ticket_id})
        self.client.login(username='user_with_manager_perm', password='12test12')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 404)

    def test_unauthenticated_api_get_ticket_status(self):
        target_url = reverse("inbox_ticket_api_status", kwargs={"pk": self.undebited_ticket.pk})
        response = self.client.get(target_url)
        self.assertRedirects(
            response,
            '/accounts/login/?next={}'.format(target_url),
            status_code=302,
            target_status_code=200
        )

    def test_authenticated_api_get_ticket_status(self):
        target_url = reverse("inbox_ticket_api_status", kwargs={"pk": self.undebited_ticket.pk})
        self.client.login(username='user_with_manager_perm_not_creator', password='12test12')
        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Status'], 'testStatus')
        self.assertEqual(response.data['CityRecipient'], 'testCity')

    def test_api_refresh_ticket_status(self):
        target_url = reverse("inbox_ticket_api_status", kwargs={"pk": self.undebited_ticket.pk})
        self.client.login(username='user_with_manager_perm_not_creator', password='12test12')
        response = self.client.post(target_url, {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Status'], 'testStatus')
        self.assertEqual(response.data['WarehouseRecipient'], 'testRecipient')

    def test_unauthenticated_inbox_api(self):
        target_url = reverse("inbox_api")
        response = self.client.get(target_url)
        self.assertRedirects(
            response,
            '/accounts/login/?next={}'.format(target_url),
            status_code=302,
            target_status_code=200
        )

    def test_authenticated_inbox_api_get_data(self):
        target_url = reverse("inbox_api")
        self.client.login(username='user_with_manager_perm', password='12test12')
        response = self.client.post(target_url, {'serial': 5555555, 'deliver_name': "Новая Почта"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Status'], 'testStatus')
        self.assertEqual(response.data['CityRecipient'], 'testCity')
