# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

import kvstore
from kvstore.tests.models import Article


class KVStoreBaseTestCase(TestCase):

    # HACK: Reset registry after each test method
    def tearDown(self):
        # Remove tag descriptor from the Article model
        del Article.kvstore

        # Clear the registry
        del kvstore.registry[:]
