from setuptools import setup, find_packages

setup(name='kvstore',
    packages=find_packages(),  
    description = 'Django allows you to easily tag a django db object with key/value pairs.',
    url = 'http://github.com/infoscout/kvstore',
    version = '0.1dev',    
    install_requires=[
        'django>=1.4',
    ]
)

