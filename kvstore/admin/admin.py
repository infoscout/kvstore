from django.conf.urls import patterns, url

from isc_admin.admin_site import AdminApp

from kvstore.admin.views import upload


class KVStoreAdminApp(AdminApp):
    def get_urls(self):
        urls = patterns(
            '',
            url(r'^kvstore/upload/?$', self.admin_view(upload), name="kvstore_upload"),
        )
        return urls
