from django.test import TestCase

import kvstore
from kvstore.tests.models import Article


class KVStoreTestCase(TestCase):

    def setUp(self):
        # super(KVStoreTestCase, self).setUp()
        kvstore.register(Article)
        self.article = Article.objects.create(title="Test")

    def test_kvstore(self):
        # Add tag
        self.article.kvstore.set('foo', 'bar')
        self.assertEqual('bar', self.article.kvstore.get('foo'))
        self.assertDictEqual({'foo': 'bar'}, self.article.kvstore.all())

        # Add tags via dict
        self.article.kvstore.set({'foo2': 'bar2'})
        self.assertTrue(self.article.kvstore.has('foo2'))

        # Update existing tag
        self.article.kvstore.set('foo', 'baz')
        self.assertEqual('baz', self.article.kvstore.get('foo'))

        # Delete tag
        self.article.kvstore.delete('foo2')
        self.assertFalse(self.article.kvstore.has('foo2'))

        # Delete all tags
        self.article.kvstore.delete_all()
        self.assertDictEqual(self.article.kvstore.all(), {})
