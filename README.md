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


## Other Fields

**JSONCharField**

If you need to use your JSON field in an index or other constraint, you can use **JSONCharField** which subclasses **CharField** instead of **TextField**. Note you'll need to specify a **max_length** parameter if you use this field.
