from unittest import TestCase
from django.test import TestCase,Client
from django.urls import reverse
from .models import Consumer,Item,ConsumerOrder
class Test_home_view(TestCase):
    def test_consumer_home(self):
        client=Client()
        response=client.get(reverse('consumer-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'ecom/customer_home.html')