# django-jsonfield

django-jsonfield is a reusable Django field that allows you to store validated JSON in your model.

It silently takes care of serialization. To use, simply add the field to one of your models.

===

## Install

    pip install jsonfield


## Usage

    from django.db import models
    from jsonfield import JSONField

    class MyModel(models.Model):
      json = JSONField()


## Advanced Usage

By default python deserializes json into dict objects. This behavior differs from the standard json behavior because python dicts do not have ordered keys.

To overcome this limitation and keep the sort order of OrderedDict keys the deserialisation can be adjusted on model initialisation:

    import collections
    class MyModel(models.Model):
      json = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})


## Other Fields

**jsonfield.JSONCharField**

If you need to use your JSON field in an index or other constraint, you can use **JSONCharField** which subclasses **CharField** instead of **TextField**. You'll also need to specify a **max_length** parameter if you use this field.

## Contact

http://bradjasper.com
