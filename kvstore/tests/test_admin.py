# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin.sites import AdminSite
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory, TestCase
import mock

from kvstore.admin.admin import KVStoreAdminApp
from kvstore.admin.views import upload
from kvstore.tests.models import Article


class AdminTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()

    def test_admin_get_urls(self):
        admin_app = KVStoreAdminApp(Article, self.site)
        urls = admin_app.get_urls()
        self.assertEqual(len(urls), 1)

    def test_admin_get_request(self):
        # Create an instance of a GET request
        request = self.factory.get('kvstore/upload/')
        # Test upload() as if it were deployed at /kvstore/upload/
        response = upload(request)
        self.assertEqual(response.status_code, 200)

    @mock.patch('kvstore.admin.views.messages')
    def test_admin_post_request(self, mock_messages):
        some_content_type = ContentType.objects.all()[0].id
        some_input = '1, cool, very'

        # Create an instance of a POST request
        request = self.factory.post(
            'kvstore/upload/',
            {'object': some_content_type, 'input': some_input},
        )
        # Test upload() as if it were deployed at /kvstore/upload/
        response = upload(request)
        self.assertEqual(response.status_code, 200)
