import kvstore

from django.test import TestCase
from kvstore.tests.models import Article, ArticleWithKVstore
from kvstore.accessor import TagDescriptor

class RegisterTestCase(TestCase):

    def setUp(self):
        pass

    def test_register_multiple_models(self):
        """Attempts to register the same model multiple times"""
        for _ in range(3):
            kvstore.register(Article)

        self.assertEqual(1, len(kvstore.registry))

    def test_model_hasattr(self):
        """Attempts to add a kvstore attribute to model that already has one"""
        
        setattr(ArticleWithKVstore, 'kvstore', TagDescriptor())
        self.assertRaises(AttributeError, kvstore.register, ArticleWithKVstore)
