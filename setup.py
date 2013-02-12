from distutils.core import setup
from distutils.core import Command


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(DATABASES={'default': {'NAME': ':memory:',
            'ENGINE': 'django.db.backends.sqlite3'}},
            INSTALLED_APPS=('jsonfield',))
        from django.core.management import call_command
        call_command('test', 'jsonfield')


setup(name='jsonfield',
      version='0.9.5',
      packages=['jsonfield'],
      license='MIT',
      long_description="A reusable Django field that allows you to store validated JSON in your model.",
      cmdclass={'test': TestCommand}
      )
