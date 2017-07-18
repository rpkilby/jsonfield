import copy
from django.db import models
from django.utils.translation import ugettext_lazy as _
try:
    from django.utils import six
except ImportError:
    import six

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.forms import fields
try:
    from django.forms.utils import ValidationError
except ImportError:
    from django.forms.util import ValidationError

from .subclassing import SubfieldBase
from .encoder import JSONEncoder


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

        # Trap cleaning errors & bubble them up as JSON errors
        try:
            return super(JSONFormFieldBase, self).clean(value)
        except TypeError:
            raise ValidationError(_("Enter valid JSON"))


class JSONFormField(JSONFormFieldBase, fields.CharField):
    pass


class JSONCharFormField(JSONFormFieldBase, fields.CharField):
    pass


class JSONFieldBase(models.Field):

    def __init__(self, *args, **kwargs):
        self.dump_kwargs = kwargs.pop('dump_kwargs', {
            'cls': JSONEncoder,
            'separators': (',', ':')
        })
        self.load_kwargs = kwargs.pop('load_kwargs', {})

        super(JSONFieldBase, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return json.loads(value, **self.load_kwargs)

    def to_python(self, value):
        if isinstance(value, unicode):
            return json.loads(value, **self.load_kwargs)
        else:
            return value

    def get_prep_value(self, value):
        """Convert JSON object to a string"""
        if self.null and value is None:
            return None
        return json.dumps(value, **self.dump_kwargs)

    def _get_val_from_obj(self, obj):
        # This function created to replace Django deprecated version
        # https://code.djangoproject.com/ticket/24716
        if obj is not None:
            return getattr(obj, self.attname)
        else:
            return self.get_default()

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
        return json.dumps(value, **kwargs)


class JSONCharField(JSONFieldBase, models.CharField):
    """JSONCharField is a generic textfield that serializes/deserializes JSON objects,
    stored in the database like a CharField, which enables it to be used
    e.g. in unique keys"""
    form_class = JSONCharFormField


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^jsonfield\.fields\.(JSONField|JSONCharField)"])
except ImportError:
    pass
