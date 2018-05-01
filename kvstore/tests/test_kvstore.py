import kvstore
from kvstore.tests.models import Article
from kvstore.tests.utils import KVStoreBaseTestCase
from kvstore.models import Tag
from django.contrib.contenttypes.models import ContentType


class KVStoreTestCase(KVStoreBaseTestCase):

    def setUp(self):
        # super(KVStoreTestCase, self).setUp()
        kvstore.register(Article)
        self.article = Article.objects.create(title="Test")
        self.content_obj = ContentType.objects.filter(app_label="sessions")[0]
        self.tag = Tag.objects.create(content_object=self.content_obj,
                                      object_id=1, key="cool", value="very")


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

    def test_tag_unicode(self):
        tag_unicode = self.tag.__unicode__()
        self.assertEqual('session - cool - very', tag_unicode)
