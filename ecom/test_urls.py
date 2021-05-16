from django.test import SimpleTestCase
from django.urls import  reverse,resolve
from .views import afterlogin_view,consumer_home


class TestUrls(SimpleTestCase):
    def test_consumer_home_urls(self):
        url=reverse('consumer-home')
        self.assertEquals(resolve(url).func,consumer_home)
