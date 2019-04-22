from django.contrib import admin

from kvstore.admin.admin import KVStoreAdminApp
from kvstore.models import Tag

admin.site.register(Tag, KVStoreAdminApp)
