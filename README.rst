django-jsonfield
----------------

**django-jsonfield is looking for maintainers that want to help keep the software up-to-date with bug patches & Django versions. Please email bjasper@gmail.com if interested.**

django-jsonfield is a reusable Django field that allows you to store validated JSON in your model.

It silently takes care of serialization. To use, simply add the field to one of your models.

Python 3 & Django 1.8 supported!

**Use PostgreSQL?** 1.0.0 introduced a breaking change to the underlying data type, so if you were using < 1.0.0 please read https://github.com/bradjasper/django-jsonfield/issues/57 before upgrading.

**Note:** There are a couple of JSONField's for Django. This one is django-jsonfield here on GitHub but jsonfield on PyPi.

**Note:** Semvar is followed after the 1.0 released.


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

django-jsonfield supports Python 2.7 to Python 3.4 and Django 1.4 to 1.8

**Why doesn't it support Python 2.6?**

You actually might be OK if you don't use an OrderedDict, but there are some issues with the simplejson API that make it cumbersome to support.

**Why doesn't it support Django 1.3?**

There was a bug that could only be fixed by a feature in Django 1.4. `Read More`_ if you're interested in the details.

.. _Read More: https://github.com/bradjasper/django-jsonfield/issues/33


Travis CI
---------

.. image:: https://travis-ci.org/bradjasper/django-jsonfield.png?branch=master


Contact
-------
Web: http://bradjasper.com

Twitter: `@bradjasper`_

Email: `contact@bradjasper.com`_



.. _contact@bradjasper.com: mailto:contact@bradjasper.com
.. _@bradjasper: https://twitter.com/bradjasper

Changes
-------

v1.0.3, 2/23/2015 -- Added fix to setup.py to allow PIP install

v1.0.2, 2/9/2015 -- Re-added fix for south migration bug

v1.0.1, 2/2/2015 -- Added Django 1.8 support

v1.0.0, 9/4/2014 -- Removed native JSON datatype support for PostgreSQL (breaking change) & added Python 3.4 to tests

v0.9.23, 9/3/2014 -- Allowed tests to run in older versions of Django

v0.9.22, 7/10/2014 -- Added Django 1.7 support

v0.9.21, 5/26/2014 -- Added better support for Python 3 and tests for regex lookups

v0.9.20, 11/14/2013 -- Fixed load_kwargs on form fields, added Django 1.6 to automated tests

v0.9.19, 09/18/2013 -- Fixed changes to django.six.with_metaclass that broke django-jsonfield for Django 1.6

v0.9.18, 08/23/2013 -- Fixed bugs with South datamigration

v0.9.17, 06/07/2013 -- Fixed bugs in JSONCharField admin form

v0.9.14/15/16, 04/29/2013 -- Python 3 support added!

v0.9.11/12/13, 03/26/2013 -- PyPi changes

v0.9.9/10/11, 03/21/2013 -- PyPi changes

v0.9.8, 03/21/2013 -- Added support for native PostgreSQL JSON data type

v0.9.7, 03/21/2013 -- Fix bug #33 where JSONField didn't correctly store some values inside of
strings

