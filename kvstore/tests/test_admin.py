# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io

try:
    import mock
except ImportError:
    from unittest import mock

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import Client, RequestFactory, TestCase
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from kvstore.admin.admin import KVStoreAdminApp
from kvstore.admin.views import upload, upload_bulk
from kvstore.models import Tag
from kvstore.tests.models import Article


class CustomAdminViewTestCase(TestCase):
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
        self.assertEqual(len(urls), 3)

    def test_admin_get_custom_admin_view(self):
        request = self.factory.get("kvstore/upload/")
        request.user = self.user
        response = upload(request)
        self.assertEqual(response.status_code, 200)


class AdminBulkUploadTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="admin")
        cls.user.is_superuser = True
        cls.user.save()

    def setUp(self):
        self.factory = RequestFactory()
        self.site = AdminSite()

    @mock.patch("kvstore.admin.views.messages")
    def test_bulk_upload(self, mock_messages):
        # Arrange
        some_content_type = ContentType.objects.all()[0].id
        some_input = "1, cool, very"
        post_json = {
            "object": some_content_type,
            "allow_overwrite": True,
            "input": some_input
        }
        request = self.factory.post("kvstore/upload_bulk/", post_json)
        request.user = self.user

        # Act
        response = upload_bulk(request)

        # Assert
        self.assertEqual(response.status_code, 200)

        tags_created = Tag.objects.all()
        self.assertEqual(len(tags_created), 1)

        tag = tags_created[0]
        self.assertEqual(tag.content_type_id, 1)
        self.assertEqual(tag.key, "cool")
        self.assertEqual(tag.value, "very")


class AdminUploadCSVTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="12345"
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username="admin", password="12345")

    @mock.patch("kvstore.admin.views.messages")
    def test_csv_upload_with_header(self, mock_messages):
        # Arrange
        some_content_type = ContentType.objects.all()[0].id
        post_json = {
            "object": some_content_type,
            "file": io.BytesIO(b"1, key, value\n1, key2, value2"),
        }

        # Act
        response = self.client.post(
            reverse("admin:kvstore_upload_csv"), post_json, format="multipart"
        )

        # Assert
        self.assertEqual(response.status_code, 200)

        tags_created = Tag.objects.all()
        self.assertEqual(len(tags_created), 2)

        tag = tags_created[0]
        self.assertEqual(tag.content_type_id, 1)
        self.assertEqual(tag.key, "key")
        self.assertEqual(tag.value, "value")

        tag = tags_created[1]
        self.assertEqual(tag.content_type_id, 1)
        self.assertEqual(tag.key, "key2")
        self.assertEqual(tag.value, "value2")
