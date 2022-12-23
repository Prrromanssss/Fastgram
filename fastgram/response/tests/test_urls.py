from django.test import Client, TestCase
from django.urls import reverse


class StaticUrlTests(TestCase):
    def test_response_endpoints(self):
        response = Client().get(reverse('response:list_responses'))
        self.assertEqual(response.status_code, 200)
