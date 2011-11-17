from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json


class JSONField(models.TextField):
    """JSONField is a generic textfield that serializes/unserializes JSON objects"""

    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.dump_kwargs = kwargs.pop('dump_kwargs', {'cls': DjangoJSONEncoder})
        self.load_kwargs = kwargs.pop('load_kwargs', {})

        super(JSONField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """Convert string value to JSON"""

        if isinstance(value, basestring):
            try:
                return json.loads(value, **self.load_kwargs)
            except ValueError:
                pass

        return value

    def get_db_prep_value(self, value):
        """Convert JSON object to a string"""

        if isinstance(value, basestring):
            return value

        return json.dumps(value, **self.dump_kwargs)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^jsonfield\.fields\.JSONField"])
except:
    pass
