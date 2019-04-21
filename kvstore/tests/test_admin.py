# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory, TestCase

try:
    import mock
except ImportError:
    from unittest import mock

from kvstore.admin.admin import KVStoreAdminApp
from kvstore.admin.views import upload
from kvstore.models import Tag
from kvstore.tests.models import Article


class AdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="admin")
        cls.user.is_superuser = True
        cls.user.save()

    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()

    def test_admin_get_urls(self):
        admin_app = KVStoreAdminApp(Article, self.site)
        urls = admin_app.get_urls()
        self.assertEqual(len(urls), 1)

    def test_admin_get_request(self):
        # Create an instance of a GET request
        request = self.factory.get("kvstore/upload/")
        request.user = self.user
        # Test upload() as if it were deployed at /kvstore/upload/
        response = upload(request)
        self.assertEqual(response.status_code, 200)

    @mock.patch("kvstore.admin.views.messages")
    def test_admin_post_request(self, mock_messages):
        # Arrange
        some_content_type = ContentType.objects.all()[0].id
        some_input = "1, cool, very"
        post_json = {"object": some_content_type, "input": some_input}
        request = self.factory.post("kvstore/upload/", post_json)
        request.user = self.user

        # Act
        response = upload(request)

        # Assert
        self.assertEqual(response.status_code, 200)

        tags_created = Tag.objects.all()
        self.assertEqual(len(tags_created), 1)

        tag = tags_created[0]
        self.assertEqual(tag.content_type_id, 1)
        self.assertEqual(tag.key, "cool")
        self.assertEqual(tag.value, "very")

    @mock.patch("kvstore.admin.views.messages")
    def test_admin_post_request_update_existing_entry(self, mock_messages):
        # Arrange
        some_content_type = ContentType.objects.all()[0].id
        some_input = "1, cool, very"
        post_json = {"object": some_content_type, "input": some_input}
        request = self.factory.post("kvstore/upload/", post_json)
        request.user = self.user
        response = upload(request)

        # Act (update key)
        updated_key = "extremely"
        some_input = "1, cool, {0}".format(updated_key)
        post_json = {"object": some_content_type, "input": some_input}
        request = self.factory.post("kvstore/upload/", post_json)
        request.user = self.user
        response = upload(request)

        # Assert
        self.assertEqual(response.status_code, 200)

        tags_created = Tag.objects.all()
        self.assertEqual(len(tags_created), 1)

        tag = tags_created[0]
        self.assertEqual(tag.content_type_id, 1)
        self.assertEqual(tag.key, "cool")
        self.assertEqual(tag.value, updated_key)
