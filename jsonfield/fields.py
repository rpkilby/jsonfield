import copy
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import ugettext_lazy as _

try:
    from django.utils import six
except ImportError:
    import six

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.forms.fields import Field
from django.forms.util import ValidationError

from .subclassing import SubfieldBase


class JSONFormField(Field):
    def clean(self, value):

        if not value and not self.required:
            return None

        value = super(JSONFormField, self).clean(value)

        if isinstance(value, six.string_types):
            try:
                json.loads(value)
            except ValueError:
                raise ValidationError(_("Enter valid JSON"))
        return value


class JSONFieldBase(six.with_metaclass(SubfieldBase, base=models.Field)):

    def __init__(self, *args, **kwargs):
        self.dump_kwargs = kwargs.pop('dump_kwargs', {
            'cls': DjangoJSONEncoder,
            'separators': (',', ':')
        })
        self.load_kwargs = kwargs.pop('load_kwargs', {})

        super(JSONFieldBase, self).__init__(*args, **kwargs)

    def pre_init(self, value, obj):
        """Convert a string value to JSON only if it needs to be deserialized.
        
        SubfieldBase meteaclass has been modified to call this method instead of
        to_python so that we can check the obj state and determine if it needs to be
        deserialized"""

        if obj._state.adding and obj.pk is not None:
            if isinstance(value, six.string_types):
                try:
                    return json.loads(value, **self.load_kwargs)
                except ValueError:
                    raise ValidationError(_("Enter valid JSON"))

        return value

    def to_python(self, value):
        """The SubfieldBase metaclass calls pre_init instead of to_python, however to_python
        is still necessary for Django's deserializer"""
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        """Convert JSON object to a string"""
        if self.null and value is None:
            return None
        return json.dumps(value, **self.dump_kwargs)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value, None)

    def value_from_object(self, obj):
        value = super(JSONFieldBase, self).value_from_object(obj)
        if self.null and value is None:
            return None
        return self.dumps_for_display(value)

    def dumps_for_display(self, value):
        return json.dumps(value, **self.dump_kwargs)

    def formfield(self, **kwargs):

        if "form_class" not in kwargs:
            kwargs["form_class"] = JSONFormField

        field = super(JSONFieldBase, self).formfield(**kwargs)

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

    def db_type(self, connection):
        if connection.vendor == 'postgresql' and connection.pg_version >= 90200:
            return 'json'
        else:
            return super(JSONFieldBase, self).db_type(connection)

class JSONField(JSONFieldBase, models.TextField):
    """JSONField is a generic textfield that serializes/unserializes JSON objects"""
    def dumps_for_display(self, value):
        kwargs = { "indent": 2 }
        kwargs.update(self.dump_kwargs)
        return json.dumps(value, **kwargs)


class JSONCharField(JSONFieldBase, models.CharField):
    """JSONCharField is a generic textfield that serializes/unserializes JSON objects,
    stored in the database like a CharField, which enables it to be used
    e.g. in unique keys"""


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^jsonfield\.fields\.(JSONField|JSONCharField)"])
except ImportError:
    pass
