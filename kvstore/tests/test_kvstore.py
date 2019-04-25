# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
import six

import kvstore
from kvstore.models import Tag
from kvstore.tests.models import Article
from kvstore.tests.utils import KVStoreBaseTestCase


class KVStoreTestCase(KVStoreBaseTestCase):

    def setUp(self):
        kvstore.register(Article)
        self.article = Article.objects.create(title="Test")
        self.content_type = ContentType.objects.filter(app_label="sessions")[0]
        self.tag = Tag.objects.create(
            content_object=self.content_type,
            object_id=1,
            key="cool",
            value="very"
        )

    def test_kvstore_add_tag(self):
        self.article.kvstore.set('foo', 'bar')

        self.assertEqual('bar', self.article.kvstore.get('foo'))
        self.assertDictEqual({'foo': 'bar'}, self.article.kvstore.all())

    def test_kvstore_add_tag_as_dict(self):
        self.article.kvstore.set({'foo2': 'bar2'})

        self.assertTrue(self.article.kvstore.has('foo2'))

    def test_kvstore_update_existing_tag(self):
        self.article.kvstore.set('foo', 'bar')

        self.article.kvstore.set('foo', 'baz')

        self.assertEqual('baz', self.article.kvstore.get('foo'))

    def test_delete_tag(self):
        self.article.kvstore.set({'foo2': 'bar2'})

        self.article.kvstore.delete('foo2')

        self.assertFalse(self.article.kvstore.has('foo2'))

    def test_delete_all_tags(self):
        self.article.kvstore.set('foo', 'bar')
        self.article.kvstore.set({'foo2': 'bar2'})

        self.article.kvstore.delete_all()

        self.assertDictEqual(self.article.kvstore.all(), {})

    def test_tag_str(self):
        tag_str = six.text_type(self.tag)
        self.assertEqual('session - cool - very', tag_str)
