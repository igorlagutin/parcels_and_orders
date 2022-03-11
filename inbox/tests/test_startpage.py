from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class StartPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='12test12',
            email='test@example.com'
        )
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_satrtpage_redirect_to_login_page_for_not_auth(self):
        response = self.client.get('/')
        self.assertRedirects(
            response,
            '/accounts/login/?next=/',
            status_code=302,
            target_status_code=200
        )

    def test_satrtpage_allow_authentificated(self):
        self.client.login(username='test', password='12test12')
        response = self.client.get(reverse('startpage'))
        self.assertEqual(response.status_code, 200)