import json

from django.forms import ValidationError, fields
from django.utils.translation import gettext_lazy as _

from .json import checked_loads


class JSONField(fields.CharField):
    def __init__(self, *args, dump_kwargs=None, load_kwargs=None, **kwargs):
        self.dump_kwargs = dump_kwargs if dump_kwargs else {}
        self.load_kwargs = load_kwargs if load_kwargs else {}

        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if self.disabled:
            return value

        if value in self.empty_values:
            return None

        try:
            return checked_loads(value, **self.load_kwargs)
        except json.JSONDecodeError:
            raise ValidationError(_("Enter valid JSON."))

    def prepare_value(self, value):
        return json.dumps(value, **self.dump_kwargs)
