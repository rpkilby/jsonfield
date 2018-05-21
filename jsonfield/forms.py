import json

from django.forms import ValidationError, fields
from django.utils import six
from django.utils.translation import ugettext_lazy as _


class JSONFieldMixin(object):
    def __init__(self, *args, **kwargs):
        self.load_kwargs = kwargs.pop('load_kwargs', {})
        super(JSONFieldMixin, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, six.string_types) and value:
            try:
                return json.loads(value, **self.load_kwargs)
            except ValueError:
                raise ValidationError(_("Enter valid JSON."))
        return value

    def clean(self, value):
        if not value and not self.required:
            return None

        # Trap cleaning errors & bubble them up as JSON errors
        try:
            return super(JSONFieldMixin, self).clean(value)
        except TypeError:
            raise ValidationError(_("Enter valid JSON."))


class JSONField(JSONFieldMixin, fields.CharField):
    pass
