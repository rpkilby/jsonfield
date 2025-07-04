jsonfield
=========

.. image:: https://github.com/rpkilby/jsonfield/actions/workflows/main.yml/badge.svg
  :target: https://github.com/rpkilby/jsonfield/actions/workflows/main.yml
.. image:: https://codecov.io/gh/rpkilby/jsonfield/graph/badge.svg
  :target: https://codecov.io/gh/rpkilby/jsonfield
.. image:: https://img.shields.io/pypi/l/jsonfield.svg
  :target: https://pypi.org/project/jsonfield
.. image:: https://img.shields.io/pypi/v/jsonfield.svg
  :target: https://pypi.org/project/jsonfield
.. image:: https://img.shields.io/pypi/pyversions/jsonfield.svg
  :target: https://pypi.org/project/jsonfield

**jsonfield** is a reusable model field that allows you to store validated JSON, automatically handling
serialization to and from the database. To use, add ``jsonfield.JSONField`` to one of your models.


Deprecation & Migration to Django's native ``JSONField``
--------------------------------------------------------

Django 3.1 `introduced`_ a native ``JSONField`` that supports all database backends. As such, this package is
considered deprecated and will be archived in the future. Existing projects should migrate to Django's implemenation.

.. _introduced: https://docs.djangoproject.com/en/stable/releases/3.1/#jsonfield-for-all-supported-database-backends


Migrating from ``jsonfield.JSONField`` to ``models.JSONField`` *should* generally be straightforward. After swapping
field classes, ``python manage.py migrate`` will generate ``AlterField`` operations that should correctly migrate
your field data. However, if this does not work for your case, you will instead need to create a data migration.
The process will roughly look like:

* Rename ``<field>`` to ``old_<field>``, create migration.
* Add a nullable ``<field> = models.JSONField(null=True, ...)``, create migration.
* Create an empty migration file, add  ``RunPython`` operation that reserializes
  the ``old_<field>`` data into the new ``<field>``.
* Update ``<field>`` to not nullable, delete ``old_<field>``, create migration.
* Manually combine the operations into a single migration file.

Examples can be found in the `migration-example`_ project.

.. _migration-example: https://github.com/rpkilby/jsonfield/tree/master/migration-example/


Installation
------------

.. code-block:: python

    pip install jsonfield


Usage
-----

.. code-block:: python

    from django.db import models
    from jsonfield import JSONField

    class MyModel(models.Model):
        json = JSONField()


Querying
--------

As stated above, ``JSONField`` is not intended to provide extended querying capabilities.
That said, you may perform the same basic lookups provided by regular text fields (e.g.,
``exact`` or ``regex`` lookups). Since values are stored as serialized JSON, it is highly
recommended that you test your queries to ensure the expected results are returned.


Handling null values
--------------------

A model field's ``null`` argument typically controls whether null values may be stored in
its column by setting a not-null constraint. However, because ``JSONField`` serializes its
values (including nulls), this option instead controls *how* null values are persisted. If
``null=True``, then nulls are **not** serialized and are stored as a null value in the
database. If ``null=False``, then the null is instead stored in its serialized form.

This in turn affects how null values may be queried. Both fields support exact matching:

.. code-block:: python

    MyModel.objects.filter(json=None)

However, if you want to use the ``isnull`` lookup, you must set ``null=True``.

.. code-block:: python

    class MyModel(models.Model):
        json = JSONField(null=True)

    MyModel.objects.filter(json__isnull=True)

Note that as ``JSONField.null`` does not prevent nulls from being stored, achieving this
must instead be handled with a validator.


Advanced Usage
--------------

By default python deserializes json into dict objects. This behavior differs from the standard json
behavior  because python dicts do not have ordered keys. To overcome this limitation and keep the
sort order of OrderedDict keys the deserialisation can be adjusted on model initialisation:

.. code-block:: python

    import collections

    class MyModel(models.Model):
        json = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})


Other Fields
------------

**jsonfield.JSONCharField**

Subclasses **models.CharField** instead of **models.TextField**.


Running the tests
-----------------

The test suite requires ``tox``.

.. code-block:: shell

    $ pip install tox


Then, run the ``tox`` command, which will run all test jobs.

.. code-block:: shell

    $ tox

Or, to test just one job (for example Django 5.2 on Python 3.13):

.. code-block:: shell

    $ tox -e py313-django52


Release Process
---------------

* Update changelog
* Update package version in setup.py
* Check supported versions in setup.py and readme
* Create git tag for version
* Upload release to PyPI test server
* Upload release to official PyPI server

.. code-block:: shell

    $ pip install -U pip setuptools wheel twine
    $ rm -rf dist/ build/
    $ python setup.py sdist bdist_wheel
    $ twine upload -r test dist/*
    $ twine upload dist/*


Changes
-------

Take a look at the `changelog`_.

.. _changelog: https://github.com/rpkilby/jsonfield/blob/master/CHANGES.rst
