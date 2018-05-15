# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import Command, find_packages, setup


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
            INSTALLED_APPS=(
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.messages',
                'django.contrib.sessions',
                'django.contrib.humanize',
                'kvstore',
                'kvstore.tests',
            ),
            TEMPLATES=[
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',  # noqa: E501
                    'APP_DIRS': True,
                    'OPTIONS': {
                        'context_processors': [
                            'django.contrib.auth.context_processors.auth',
                            'django.contrib.messages.context_processors.messages',  # noqa: E501
                        ],
                    },
                },
            ],
            MIDDLEWARE=(
                'django.middleware.common.CommonMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
            ),
            MIDDLEWARE_CLASSES=(
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
            ),  # Django < 1.10
            ROOT_URLCONF='kvstore.tests.urls',
        )
        django.setup()
        call_command('test', 'kvstore')


setup(
    name='kvstore',
    packages=find_packages(),
    include_package_data=True,
    description=(
        "Django allows you to easily tag a django db object"
        "with key/value pairs."
    ),
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
