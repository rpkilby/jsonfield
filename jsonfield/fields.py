from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json

try:
	import cPickle as pickle
except ImportError:
	import pickle



class JSONField(models.TextField):
    """JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly"""

    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""

        if value == "":
            return None

        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            pass

        return value

    def get_db_prep_save(self, value, connection):
        """Convert our JSON object to a string before we save"""

        if not value or value == "":
            return None

        if isinstance(value, (dict, list)):
            value = json.dumps(value, cls=DjangoJSONEncoder)

        return super(JSONField, self).get_db_prep_save(value, connection)


class PickledObject(str):
	"""A subclass of string so it can be told whether a string is
	   a pickled object or not (if the object is an instance of this class
	   then it must [well, should] be a pickled one)."""
	pass

class PickledObjectField(models.Field):
	__metaclass__ = models.SubfieldBase
	
	def to_python(self, value):
		if isinstance(value, PickledObject):
			# If the value is a definite pickle; and an error is raised in de-pickling
			# it should be allowed to propogate.
			return pickle.loads(str(value))
		else:
			try:
				return pickle.loads(str(value))
			except:
				# If an error was raised, just return the plain value
				return value
	
	def get_db_prep_save(self, value, connection):
		if value is not None and not isinstance(value, PickledObject):
			value = PickledObject(pickle.dumps(value))
		return value
	
	def get_internal_type(self): 
		return 'TextField'
	
	def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
		if lookup_type == 'exact':
			value = self.get_db_prep_save(value, None)
			return super(PickledObjectField, self).get_db_prep_lookup(lookup_type, value, connection,
                            prepared)
		elif lookup_type == 'in':
			value = [self.get_db_prep_save(v, None) for v in value]
			return super(PickledObjectField, self).get_db_prep_lookup(lookup_type, value, connection,
                            prepared)
		else:
			raise TypeError('Lookup type %s is not supported.' % lookup_type)
