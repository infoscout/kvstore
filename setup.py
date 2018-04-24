from setuptools import Command,find_packages, setup


with open('VERSION', 'r') as f:
    version = f.read().strip()


class TestCommand(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import django
        from django.conf import settings
        from django.core.management import call_command

        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3',
                },
            },
            # DEFAULT_INDEX_TABLESPACE='',
            INSTALLED_APPS=(
                'django.contrib.auth',
                'django.contrib.contenttypes',
                # 'django.contrib.sessions',
                'kvstore',
                'kvstore.tests',
            ),
            MIDDLEWARE=(),
            # MIDDLEWARE_CLASSES=(),  # Django < 1.10
            # ROOT_URLCONF='saml_service_provider.urls',
            # AUTHENTICATION_BACKENDS=['isc_saml.auth_backend.ISCSAMLBackend']
        )
        django.setup()
        call_command('test', 'kvstore')


setup(
    name='kvstore',
    packages=find_packages(),
    include_package_data=True,
    description='Django allows you to easily tag a django db object with key/value pairs.',
    url='http://github.com/infoscout/kvstore',
    version=version,
    install_requires=[
        'Django>=1.8',
    ],
    tests_require=[
        'mock',
    ],
    cmdclass={'test': TestCommand}
)
