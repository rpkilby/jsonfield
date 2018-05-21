import copy
import json

from django.db import models
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from . import forms
from .encoder import JSONEncoder


class JSONFieldMixin(models.Field):
    form_class = forms.JSONField

    def __init__(self, *args, dump_kwargs=None, load_kwargs=None, **kwargs):
        self.dump_kwargs = dump_kwargs if dump_kwargs is not None else {
            'cls': JSONEncoder,
            'separators': (',', ':')
        }
        self.load_kwargs = load_kwargs if load_kwargs is not None else {}

        super(JSONFieldMixin, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        if self.dump_kwargs is not None:
            kwargs['dump_kwargs'] = self.dump_kwargs
        if self.load_kwargs is not None:
            kwargs['load_kwargs'] = self.load_kwargs
        return name, path, args, kwargs

    def to_python(self, value):
        if self.null and value is None:
            return None

        if not isinstance(value, (str, bytes, bytearray)):
            return value

        try:
            return json.loads(value, **self.load_kwargs)
        except ValueError:
            raise ValidationError(_("Enter valid JSON."))

    def from_db_value(self, value, expression, connection, context=None):
        if self.null and value is None:
            return None
        return json.loads(value, **self.load_kwargs)

    def get_prep_value(self, value):
        """Convert JSON object to a string"""
        if self.null and value is None:
            return None
        return json.dumps(value, **self.dump_kwargs)

    def value_from_object(self, obj):
        value = super(JSONFieldMixin, self).value_from_object(obj)
        if self.null and value is None:
            return None
        return json.dumps(value, **self.dump_kwargs)

    def formfield(self, **kwargs):
        if "form_class" not in kwargs:
            kwargs["form_class"] = self.form_class

        field = super(JSONFieldMixin, self).formfield(**kwargs)

        if isinstance(field, forms.JSONFieldMixin):
            field.load_kwargs = self.load_kwargs

        if not field.help_text:
            field.help_text = "Enter valid JSON."

        return field

    def get_default(self):
        """
        Returns the default value for this field.

        The default implementation on models.Field calls force_unicode
        on the default, which means you can't set arbitrary Python
        objects as the default. To fix this, we just return the value
        without calling force_unicode on it. Note that if you set a
        callable as a default, the field will still call it. It will
        *not* try to pickle and encode it.

        """
        if self.has_default():
            if callable(self.default):
                return self.default()
            return copy.deepcopy(self.default)
        # If the field doesn't have a default, then we punt to models.Field.
        return super(JSONFieldMixin, self).get_default()


class JSONField(JSONFieldMixin, models.TextField):
    """JSONField is a generic textfield that serializes/deserializes JSON objects"""


class JSONCharField(JSONFieldMixin, models.CharField):
    """JSONCharField is a generic textfield that serializes/deserializes JSON objects"""
