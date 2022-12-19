from django.test import Client, TestCase
from django.urls import reverse


class StaticUrlTests(TestCase):
    def test_delivery_endpoint(self):
        response = Client().get(reverse('delivery:delivery'))
        self.assertEqual(response.status_code, 200)
