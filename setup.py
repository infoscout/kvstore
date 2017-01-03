from setuptools import find_packages, setup


with open('VERSION', 'r') as f:
    version = f.read().strip()


setup(
    name='kvstore',
    packages=find_packages(),
    include_package_data=True,
    description='Django allows you to easily tag a django db object with key/value pairs.',
    url='http://github.com/infoscout/kvstore',
    version=version,
    install_requires=[
        'django>=1.4',
    ]
)
