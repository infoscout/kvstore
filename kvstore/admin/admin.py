from django.conf.urls.defaults import patterns, url
from isc_admin import AdminApp
from kvstore.admin.views import upload

class KVStoreAdminApp(AdminApp):
    def get_urls(self):
        urls = patterns('',
            url(r'^kvstore/upload/?$', self.admin_view(upload), name="kvstore_upload"),
        )
        return urls

#MTurkAdminApp.register(Worker, WorkerAdmin)
