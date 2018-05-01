import kvstore

from kvstore.tests.models import Article
from kvstore.tests.utils import KVStoreBaseTestCase
from kvstore.accessor import TagDescriptor


class RegisterTestCase(KVStoreBaseTestCase):

    def test_register_multiple_models(self):
        """Attempts to register the same model multiple times"""
        for _ in range(3):
            kvstore.register(Article)

        self.assertEqual(1, len(kvstore.registry))
        self.assertIn(Article, kvstore.registry)

    def test_model_hasattr(self):
        """Attempts to add a kvstore attribute to model that already has one"""
        import pdb; pdb.set_trace()
        setattr(Article, 'kvstore', TagDescriptor())
        with self.assertRaises(AttributeError):
            kvstore.register(Article)
