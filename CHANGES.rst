Changes
-------
v2.0.2, 5/18/2017
^^^^^^^^^^^^^^^^^
- Fixed issue with GenericForeignKey field

v2.0.1, 3/8/2017
^^^^^^^^^^^^^^^^
- Support upcoming Django 1.11 in test suite
- Renamed method `get_db_prep_value` to `get_prep_value`

v2.0.0, 3/4/2017
^^^^^^^^^^^^^^^^
- Added Django 1.9 and 1.10 support, removed support for Django versions older than 1.8, fixed to_python to allow for empty string

v1.0.3, 2/23/2015
^^^^^^^^^^^^^^^^^
- Added fix to setup.py to allow PIP install

v1.0.2, 2/9/2015
^^^^^^^^^^^^^^^^
- Re-added fix for south migration bug

v1.0.1, 2/2/2015
^^^^^^^^^^^^^^^^
- Added Django 1.8 support

v1.0.0, 9/4/2014
^^^^^^^^^^^^^^^^

- Removed native JSON datatype support for PostgreSQL (breaking change) & added Python 3.4 to tests

v0.9.23, 9/3/2014
^^^^^^^^^^^^^^^^^
- Allowed tests to run in older versions of Django

v0.9.22, 7/10/2014
^^^^^^^^^^^^^^^^^^
- Added Django 1.7 support

v0.9.21, 5/26/2014
^^^^^^^^^^^^^^^^^^
- Added better support for Python 3 and tests for regex lookups

v0.9.20, 11/14/2013
^^^^^^^^^^^^^^^^^^^
- Fixed load_kwargs on form fields, added Django 1.6 to automated tests

v0.9.19, 09/18/2013
^^^^^^^^^^^^^^^^^^^
- Fixed changes to django.six.with_metaclass that broke django-jsonfield for Django 1.6

v0.9.18, 08/23/2013
^^^^^^^^^^^^^^^^^^^
- Fixed bugs with South datamigration

v0.9.17, 06/07/2013
^^^^^^^^^^^^^^^^^^^
- Fixed bugs in JSONCharField admin form

v0.9.14/15/16, 04/29/2013
^^^^^^^^^^^^^^^^^^^^^^^^^
- Python 3 support added!

v0.9.11/12/13, 03/26/2013
^^^^^^^^^^^^^^^^^^^^^^^^^
- PyPi changes

v0.9.9/10/11, 03/21/2013
^^^^^^^^^^^^^^^^^^^^^^^^
- PyPi changes

v0.9.8, 03/21/2013
^^^^^^^^^^^^^^^^^^
- Added support for native PostgreSQL JSON data type

v0.9.7, 03/21/2013
^^^^^^^^^^^^^^^^^^
- Fix bug #33 where JSONField didn't correctly store some values inside of strings
