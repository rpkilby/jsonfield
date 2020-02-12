import copy
import json

import six

from django.db import models
from django.forms import fields
from django.utils.translation import ugettext_lazy as _

from .encoder import JSONEncoder
from .subclassing import SubfieldBase

try:
    from django.forms.utils import ValidationError
except ImportError:
    from django.forms.util import ValidationError


class JSONFormFieldBase(object):
    def __init__(self, *args, **kwargs):
        self.load_kwargs = kwargs.pop('load_kwargs', {})
        super(JSONFormFieldBase, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, six.string_types) and value:
            try:
                return json.loads(value, **self.load_kwargs)
            except ValueError:
                raise ValidationError(_("Enter valid JSON"))
        return value

    def clean(self, value):

        if not value and not self.required:
            return None

        # RFC 7159
        if value == 'true':
            return True
        if value == 'false':
            return False
        try:
            return int(value)
        except (TypeError, ValueError):
            pass
        try:
            return float(value)
        except (TypeError, ValueError):
            pass

        # Trap cleaning errors & bubble them up as JSON errors
        try:
            return super(JSONFormFieldBase, self).clean(value)
        except TypeError:
            raise ValidationError(_("Enter valid JSON"))


class JSONFormField(JSONFormFieldBase, fields.CharField):
    pass


class JSONCharFormField(JSONFormFieldBase, fields.CharField):
    pass


class JSONFieldBase(six.with_metaclass(SubfieldBase, models.Field)):

    def __init__(self, *args, **kwargs):
        self.dump_kwargs = kwargs.pop('dump_kwargs', {
            'cls': JSONEncoder,
            'separators': (',', ':')
        })
        self.load_kwargs = kwargs.pop('load_kwargs', {})

        super(JSONFieldBase, self).__init__(*args, **kwargs)

    def pre_init(self, value, obj):
        """Convert a string value to JSON only if it needs to be deserialized.

        SubfieldBase metaclass has been modified to call this method instead of
        to_python so that we can check the obj state and determine if it needs to be
        deserialized"""

        try:
            if obj._state.adding:
                # Make sure the primary key actually exists on the object before
                # checking if it's empty. This is a special case for South datamigrations
                # see: https://github.com/bradjasper/django-jsonfield/issues/52
                if getattr(obj, "pk", None) is not None:
                    if isinstance(value, six.string_types):
                        try:
                            return json.loads(value, **self.load_kwargs)
                        except ValueError:
                            raise ValidationError(_("Enter valid JSON"))

        except AttributeError:
            # south fake meta class doesn't create proper attributes
            # see this:
            # https://github.com/bradjasper/django-jsonfield/issues/52
            pass

        return value

    def to_python(self, value):
        """The SubfieldBase metaclass calls pre_init instead of to_python, however to_python
        is still necessary for Django's deserializer"""
        return value

    def get_prep_value(self, value):
        """Convert JSON object to a string"""
        if self.null and value is None:
            return None
        return json.dumps(value, **self.dump_kwargs)

    def value_to_string(self, obj):
        value = self.value_from_object(obj, dump=False)
        return self.get_db_prep_value(value, None)

    def value_from_object(self, obj, dump=True):
        value = super(JSONFieldBase, self).value_from_object(obj)
        if self.null and value is None:
            return None
        return self.dumps_for_display(value) if dump else value

    def dumps_for_display(self, value):
        return json.dumps(value, **self.dump_kwargs)

    def formfield(self, **kwargs):

        if "form_class" not in kwargs:
            kwargs["form_class"] = self.form_class

        field = super(JSONFieldBase, self).formfield(**kwargs)

        if isinstance(field, JSONFormFieldBase):
            field.load_kwargs = self.load_kwargs

        if not field.help_text:
            field.help_text = "Enter valid JSON"

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
        return super(JSONFieldBase, self).get_default()


class JSONField(JSONFieldBase, models.TextField):
    """JSONField is a generic textfield that serializes/deserializes JSON objects"""
    form_class = JSONFormField

    def dumps_for_display(self, value):
        kwargs = {"indent": 2}
        kwargs.update(self.dump_kwargs)
        return json.dumps(value, ensure_ascii=False, **kwargs)


class JSONCharField(JSONFieldBase, models.CharField):
    """JSONCharField is a generic textfield that serializes/deserializes JSON objects,
    stored in the database like a CharField, which enables it to be used
    e.g. in unique keys"""
    form_class = JSONCharFormField


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [r"^jsonfield\.fields\.(JSONField|JSONCharField)"])
except ImportError:
    pass
