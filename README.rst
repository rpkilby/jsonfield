django-jsonfield
----------------

**django-jsonfield is looking for maintainers that want to help keep the software up-to-date with bug patches & Django versions. Please email bjasper@gmail.com if interested.**

django-jsonfield is a reusable Django field that allows you to store validated JSON in your model.

It silently takes care of serialization. To use, simply add the field to one of your models.

Python 3 & Django 1.8 through 1.11 supported!

**Use PostgreSQL?** 1.0.0 introduced a breaking change to the underlying data type, so if you were using < 1.0.0 please read https://github.com/bradjasper/django-jsonfield/issues/57 before upgrading.

**Note:** There are a couple of JSONField's for Django. This one is django-jsonfield here on GitHub but jsonfield on PyPi.

**Note:** Semver is followed after the 1.0 release.


Install
-------

.. code-block:: python

    pip install jsonfield


Usage
-----

.. code-block:: python

    from django.db import models
    from jsonfield import JSONField

    class MyModel(models.Model):
      json = JSONField()

Advanced Usage
--------------

By default python deserializes json into dict objects. This behavior differs from the standard json behavior because python dicts do not have ordered keys.

To overcome this limitation and keep the sort order of OrderedDict keys the deserialisation can be adjusted on model initialisation:

.. code-block:: python

    import collections
    class MyModel(models.Model):
      json = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})


Other Fields
------------

**jsonfield.JSONCharField**

If you need to use your JSON field in an index or other constraint, you can use **JSONCharField** which subclasses **CharField** instead of **TextField**. You'll also need to specify a **max_length** parameter if you use this field.


Compatibility
--------------

django-jsonfield aims to support the same versions of Django currently maintained by the main Django project. See `Django supported versions`_, currently:

  * Django 1.8 (LTS) with Python 2.7, 3.3, 3.4, or 3.5
  * Django 1.9 with Python 2.7, 3.4, or 3.5
  * Django 1.10 with Python 2.7, 3.4, or 3.5

.. _Django supported versions: https://www.djangoproject.com/download/#supported-versions


Testing django-jsonfield Locally
--------------------------------

To test against all supported versions of Django:

.. code-block:: shell

    $ docker-compose build && docker-compose up

Or just one version (for example Django 1.10 on Python 3.5):

.. code-block:: shell

    $ docker-compose build && docker-compose run tox tox -e py35-1.10


Travis CI
---------

.. image:: https://travis-ci.org/bradjasper/django-jsonfield.svg?branch=master
   :target: https://travis-ci.org/bradjasper/django-jsonfield

Contact
-------
Web: http://bradjasper.com

Twitter: `@bradjasper`_

Email: `contact@bradjasper.com`_



.. _contact@bradjasper.com: mailto:contact@bradjasper.com
.. _@bradjasper: https://twitter.com/bradjasper

Changes
-------

Take a look at the `changelog`_.

.. _changelog: https://github.com/bradjasper/django-jsonfield/blob/master/CHANGES.rst
