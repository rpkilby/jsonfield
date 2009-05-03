from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from json import dumps, loads

class JSONField(models.TextField):
    """JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly"""

    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""

        if value == "":
            return None

        if isinstance(value, basestring):
            return loads(value)

        return value

    def get_db_prep_save(self, value):
        """Convert our JSON object to a string before we save"""

        if value == "":
            return None

        if isinstance(value, dict):
            return dumps(value, cls=DjangoJSONEncoder)

        return super(JSONField, self).get_db_prep_save(value)
