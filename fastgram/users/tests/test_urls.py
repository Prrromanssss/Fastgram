from django.test import Client, TestCase
from django.urls import reverse


class StaticUrlTests(TestCase):
    def test_registration_endpoints(self):
        endpoints = {
            200: [
                'login',
                'password_reset',
                'password_reset_complete',
                'password_reset_done',
                'sign_up',
            ],
            302: [
                'password_change_done',
                'password_change',
                'logout',
            ],
        }

        for url in endpoints[200]:
            with self.subTest(f'Succes url - {url}'):
                response = Client().get(reverse(f'users:{url}'))
                self.assertEqual(response.status_code, 200)

        for url in endpoints[302]:
            with self.subTest(f'Succes url - {url}'):
                response = Client().get(reverse(f'users:{url}'))
                self.assertEqual(response.status_code, 302)

    def test_users_endpoints(self):
        endpoints = {
            302: [
                'profile',
            ]

        }
        for url in endpoints[302]:
            with self.subTest(f'Succes url - {url}'):
                response = Client().get(reverse(f'users:{url}'))
                self.assertEqual(response.status_code, 302)
