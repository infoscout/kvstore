from django.test import TestCase, RequestFactory
from django.conf.urls import url
from kvstore.admin.views import upload
from django.contrib.contenttypes.models import ContentType

class AdminTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_admin_get_request(self):
        # Create an instance of a GET request
        request = self.factory.get('kvstore/upload/')
        # Test upload() as if it were deployed at /kvstore/upload/
        response = upload(request)
        self.assertEqual(response.status_code, 200)

    def test_admin_post_request(self):
        post_object = ContentType.objects.all()[0].id
        post_input = '1, cool, very'

        # Create an instance of a POST request
        request = self.factory.post('kvstore/upload/', {'object':post_object, 'input':post_input})
        # Test upload() as if it were deployed at /kvstore/upload/
        response = upload(request)
        self.assertEqual(response.status_code, 200)
