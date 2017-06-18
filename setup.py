from distutils.core import Command
from setuptools import setup


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(
            DATABASES={'default': {'NAME': ':memory:', 'ENGINE': 'django.db.backends.sqlite3'}},
            INSTALLED_APPS=('jsonfield', 'django.contrib.contenttypes')
        )
        from django.core.management import call_command
        import django

        if django.VERSION[:2] >= (1, 7):
            django.setup()
        call_command('test', 'jsonfield')


setup(
    name='jsonfield',
    version='2.0.2',
    packages=['jsonfield'],
    license='MIT',
    include_package_data=True,
    author='Dan Koch',
    author_email='dmkoch@gmail.com',
    url='https://github.com/dmkoch/django-jsonfield/',
    description='A reusable Django field that allows you to store validated JSON in your model.',
    long_description=open("README.rst").read(),
    install_requires=['Django >= 1.8.0'],
    tests_require=['Django >= 1.8.0'],
    cmdclass={'test': TestCommand},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
    ],
)
