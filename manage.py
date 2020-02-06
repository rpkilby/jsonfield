#!/usr/bin/env python
import os
import sys

try:
    me = os.path.realpath(os.readlink(__file__))
except OSError:
    me = os.path.realpath(__file__)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    import logging

    log = logging.getLogger('raven.contrib.django.client.DjangoClient')

    from django.core.management import execute_from_command_line

    debug_on_error = '--pdb' in sys.argv
    args = [a for a in sys.argv if a != '--pdb']

    execute_from_command_line(args)
