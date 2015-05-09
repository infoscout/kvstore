from setuptools import find_packages
from isc_ops.setup_tools import setup, current_version

setup(name='kvstore',
    packages=find_packages(),  
    include_package_data=True,
    description = 'Django allows you to easily tag a django db object with key/value pairs.',
    url = 'http://github.com/infoscout/kvstore',
    version = current_version(),    
    install_requires=[
        'django>=1.4',
    ]
)

