from django.test import Client, TestCase
from django.urls import reverse


class TaskPagesTests(TestCase):
    def test_users_shown_correct_context_sign_up(self):
        response = Client().get(reverse('users:sign_up'))
        self.assertIn('form', response.context)
