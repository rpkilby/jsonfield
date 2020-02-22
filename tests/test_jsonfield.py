import warnings
from collections import OrderedDict
from decimal import Decimal

from django.core.serializers import deserialize, serialize
from django.core.serializers.base import DeserializationError
from django.forms import ValidationError
from django.test import TestCase

from .models import (
    CallableDefaultModel,
    GenericForeignKeyObj,
    JSONCharModel,
    JSONModel,
    JSONModelCustomEncoders,
    JSONModelWithForeignKey,
    JSONNotRequiredModel,
    JSONRequiredModel,
    MTIChildModel,
    MTIParentModel,
    OrderedJSONModel,
    RemoteJSONModel,
)


class JSONModelWithForeignKeyTestCase(TestCase):
    def test_object_create(self):
        foreign_obj = GenericForeignKeyObj.objects.create(name='Brain')
        JSONModelWithForeignKey.objects.create(foreign_obj=foreign_obj)


class RemoteJSONFieldTests(TestCase):
    """Test JSON fields across a ForeignKey"""

    @classmethod
    def setUpTestData(cls):
        RemoteJSONModel.objects.create()

    def test_related_accessor(self):
        RemoteJSONModel.objects.get().foreign

    def test_select_related(self):
        RemoteJSONModel.objects.select_related('foreign').get()


class JSONFieldTest(TestCase):
    """JSONField Wrapper Tests"""

    json_model = JSONModel

    def test_json_field_create(self):
        """Test saving a JSON object in our JSONField"""
        json_obj = {
            "item_1": "this is a json blah",
            "blergh": "hey, hey, hey"}

        obj = self.json_model.objects.create(json=json_obj)
        new_obj = self.json_model.objects.get(id=obj.id)

        self.assertEqual(new_obj.json, json_obj)

    def test_string_in_json_field(self):
        """Test saving an ordinary Python string in our JSONField"""
        json_obj = 'blah blah'
        obj = self.json_model.objects.create(json=json_obj)
        new_obj = self.json_model.objects.get(id=obj.id)

        self.assertEqual(new_obj.json, json_obj)

    def test_float_in_json_field(self):
        """Test saving a Python float in our JSONField"""
        json_obj = 1.23
        obj = self.json_model.objects.create(json=json_obj)
        new_obj = self.json_model.objects.get(id=obj.id)

        self.assertEqual(new_obj.json, json_obj)

    def test_int_in_json_field(self):
        """Test saving a Python integer in our JSONField"""
        json_obj = 1234567
        obj = self.json_model.objects.create(json=json_obj)
        new_obj = self.json_model.objects.get(id=obj.id)

        self.assertEqual(new_obj.json, json_obj)

    def test_decimal_in_json_field(self):
        """Test saving a Python Decimal in our JSONField"""
        json_obj = Decimal(12.34)
        obj = self.json_model.objects.create(json=json_obj)
        new_obj = self.json_model.objects.get(id=obj.id)

        # here we must know to convert the returned string back to Decimal,
        # since json does not support that format
        self.assertEqual(Decimal(new_obj.json), json_obj)

    def test_json_field_modify(self):
        """Test modifying a JSON object in our JSONField"""
        json_obj_1 = {'a': 1, 'b': 2}
        json_obj_2 = {'a': 3, 'b': 4}

        obj = self.json_model.objects.create(json=json_obj_1)
        self.assertEqual(obj.json, json_obj_1)
        obj.json = json_obj_2

        self.assertEqual(obj.json, json_obj_2)
        obj.save()
        self.assertEqual(obj.json, json_obj_2)

        self.assertTrue(obj)

    def test_json_field_load(self):
        """Test loading a JSON object from the DB"""
        json_obj_1 = {'a': 1, 'b': 2}
        obj = self.json_model.objects.create(json=json_obj_1)
        new_obj = self.json_model.objects.get(id=obj.id)

        self.assertEqual(new_obj.json, json_obj_1)

    def test_json_list(self):
        """Test storing a JSON list"""
        json_obj = ["my", "list", "of", 1, "objs", {"hello": "there"}]

        obj = self.json_model.objects.create(json=json_obj)
        new_obj = self.json_model.objects.get(id=obj.id)
        self.assertEqual(new_obj.json, json_obj)

    def test_empty_objects(self):
        """Test storing empty objects"""
        for json_obj in [{}, [], 0, '', False]:
            obj = self.json_model.objects.create(json=json_obj)
            new_obj = self.json_model.objects.get(id=obj.id)
            self.assertEqual(json_obj, obj.json)
            self.assertEqual(json_obj, new_obj.json)

    def test_custom_encoder(self):
        """Test encoder_cls and object_hook"""
        value = 1 + 3j  # A complex number

        obj = JSONModelCustomEncoders.objects.create(json=value)
        new_obj = JSONModelCustomEncoders.objects.get(pk=obj.pk)
        self.assertEqual(value, new_obj.json)

    def test_django_serializers(self):
        """Test serializing/deserializing jsonfield data"""
        for json_obj in [{}, [], 0, '', False, {'key': 'value', 'num': 42,
                                                'ary': list(range(5)),
                                                'dict': {'k': 'v'}}]:
            obj = self.json_model.objects.create(json=json_obj)
            new_obj = self.json_model.objects.get(id=obj.id)
            self.assertTrue(new_obj)

        queryset = self.json_model.objects.all()
        ser = serialize('json', queryset)
        for dobj in deserialize('json', ser):
            obj = dobj.object
            pulled = self.json_model.objects.get(id=obj.pk)
            self.assertEqual(obj.json, pulled.json)

    def test_serialize_deserialize(self):
        self.json_model.objects.create(json={'foo': 'bar'})

        for f in ['python', 'json', 'xml']:
            with self.subTest(format=f):
                data = serialize(f, self.json_model.objects.all())
                deserialized, = deserialize(f, data)

                # The actual model instance is accessed as `object`.
                self.assertEqual(deserialized.object.json, {'foo': 'bar'})

    def test_serialize_deserialize_unsaved(self):
        unsaved = self.json_model(json={'foo': 'bar'})

        for f in ['python', 'json', 'xml']:
            with self.subTest(format=f):
                data = serialize(f, [unsaved])
                deserialized, = deserialize(f, data)

                # The actual model instance is accessed as `object`.
                self.assertEqual(deserialized.object.json, {'foo': 'bar'})

    def test_default_parameters(self):
        """Test providing a default value to the model"""
        model = JSONModel()
        model.json = {"check": 12}
        self.assertEqual(model.json, {"check": 12})
        self.assertEqual(type(model.json), dict)

        self.assertEqual(model.default_json, {"check": 12})
        self.assertEqual(type(model.default_json), dict)

    def test_invalid_json(self):
        # invalid json data {] in the json and default_json fields
        ser = '[{"pk": 1, "model": "tests.jsoncharmodel", ' \
            '"fields": {"json": "{]", "default_json": "{]"}}]'
        with self.assertRaises(DeserializationError) as cm:
            next(deserialize('json', ser))
        inner = cm.exception.__context__
        self.assertIsInstance(inner, ValidationError)
        self.assertEqual('Enter valid JSON.', inner.messages[0])

    def test_integer_in_string_in_json_field(self):
        """Test saving the Python string '123' in our JSONField"""
        json_obj = '123'
        obj = self.json_model.objects.create(json=json_obj)
        new_obj = self.json_model.objects.get(id=obj.id)

        self.assertEqual(new_obj.json, json_obj)

    def test_boolean_in_string_in_json_field(self):
        """Test saving the Python string 'true' in our JSONField"""
        json_obj = 'true'
        obj = self.json_model.objects.create(json=json_obj)
        new_obj = self.json_model.objects.get(id=obj.id)

        self.assertEqual(new_obj.json, json_obj)

    def test_pass_by_reference_pollution(self):
        """Make sure the default parameter is copied rather than passed by reference"""
        model = JSONModel()
        model.default_json["check"] = 144
        model.complex_default_json[0]["checkcheck"] = 144
        self.assertEqual(model.default_json["check"], 144)
        self.assertEqual(model.complex_default_json[0]["checkcheck"], 144)

        # Make sure when we create a new model, it resets to the default value
        # and not to what we just set it to (it would be if it were passed by reference)
        model = JSONModel()
        self.assertEqual(model.default_json["check"], 12)
        self.assertEqual(model.complex_default_json[0]["checkcheck"], 1212)

    def test_save_blank_object(self):
        """Test that JSON model can save a blank object as none"""

        model = JSONModel()
        self.assertEqual(model.empty_default, {})

        model.save()
        self.assertEqual(model.empty_default, {})

        model1 = JSONModel(empty_default={"hey": "now"})
        self.assertEqual(model1.empty_default, {"hey": "now"})

        model1.save()
        self.assertEqual(model1.empty_default, {"hey": "now"})

    def test_model_full_clean(self):
        instances = [
            JSONNotRequiredModel(),
            JSONModel(json={'a': 'b'}),
        ]

        for instance in instances:
            with self.subTest(instance=instance):
                instance.full_clean()
                instance.save()


class JSONCharFieldTest(JSONFieldTest):
    json_model = JSONCharModel


class MiscTests(TestCase):
    def test_load_kwargs_hook(self):
        data = OrderedDict([
            ('number', [1, 2, 3, 4]),
            ('notes', True),
            ('alpha', True),
            ('romeo', True),
            ('juliet', True),
            ('bravo', True),
        ])
        instance = OrderedJSONModel.objects.create(json=data)
        from_db = OrderedJSONModel.objects.get()

        expected_key_order = ['number', 'notes', 'alpha', 'romeo', 'juliet', 'bravo']

        # OrderedJSONModel explicitly sets `object_pairs_hook` to `OrderedDict`
        self.assertEqual(list(instance.json), expected_key_order)
        self.assertEqual(list(from_db.json), expected_key_order)
        self.assertIsInstance(from_db.json, OrderedDict)

    def test_callable_default_function(self):
        instance = CallableDefaultModel.objects.create()
        self.assertTrue(instance.json, {'example': 'data'})

        instance.refresh_from_db()
        self.assertTrue(instance.json, {'example': 'data'})

    def test_mti_deserialization(self):
        # Note that jsonfields are present on both the child and parent models.
        MTIChildModel.objects.create(
            parent_data={'parent': 'data'},
            child_data={'child': 'data'},
        )

        parent = MTIParentModel.objects.get()
        self.assertEqual(parent.parent_data, {'parent': 'data'})

        child = MTIChildModel.objects.get()
        self.assertEqual(child.parent_data, {'parent': 'data'})
        self.assertEqual(child.child_data, {'child': 'data'})

    def test_load_invalid_json(self):
        # Ensure invalid DB values don't crash deserialization.
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO tests_jsonnotrequiredmodel (json) VALUES ("foo")')

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            instance = JSONNotRequiredModel.objects.get()

        self.assertEqual(len(w), 1)
        self.assertIs(w[0].category, RuntimeWarning)
        self.assertEqual(str(w[0].message), (
            'tests.JSONNotRequiredModel.json failed to load invalid json (foo) '
            'from the database. The value has been returned as a string instead.'
        ))

        self.assertEqual(instance.json, 'foo')

    def test_resave_invalid_json(self):
        # Ensure invalid DB values are resaved as a JSON string.
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO tests_jsonnotrequiredmodel (json) VALUES ("foo")')

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            instance = JSONNotRequiredModel.objects.get()

        self.assertEqual(len(w), 1)
        self.assertEqual(instance.json, 'foo')

        # Save instance and reload from the database.
        instance.save()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            instance = JSONNotRequiredModel.objects.get()

        # No deserialization issues, as 'foo' was saved as a serialized string.
        self.assertEqual(len(w), 0)
        self.assertEqual(instance.json, 'foo')


class QueryTests(TestCase):
    def test_values_deserializes_result(self):
        JSONModel.objects.create(json={'a': 'b'})

        instance = JSONModel.objects.values('json').get()
        self.assertEqual(instance['json'], {'a': 'b'})

        data = JSONModel.objects.values_list('json', flat=True).get()
        self.assertEqual(data, {'a': 'b'})

    def test_deferred_value(self):
        JSONModel.objects.create(json={'a': 'b'})

        instance = JSONModel.objects.defer('json').get()
        self.assertEqual(instance.json, {'a': 'b'})

    def test_exact_lookup(self):
        JSONModel.objects.create(json={'foo': 'bar'})
        JSONModel.objects.create(json={'bar': 'baz'})

        self.assertEqual(JSONModel.objects.count(), 2)
        self.assertEqual(JSONModel.objects.filter(json={'foo': 'bar'}).count(), 1)

    def test_exact_none_lookup(self):
        # Note that nullable JSON fields store a 'null' value, while non-nullable
        # fields serialize as '"null"'. That said, the query prep will ensure the
        # correct value is passed.
        JSONNotRequiredModel.objects.create(json=None)
        JSONNotRequiredModel.objects.create(json=100)
        self.assertEqual(JSONNotRequiredModel.objects.count(), 2)
        self.assertEqual(JSONNotRequiredModel.objects.filter(json=None).count(), 1)

        JSONRequiredModel.objects.create(json=None)
        JSONRequiredModel.objects.create(json=100)
        self.assertEqual(JSONRequiredModel.objects.count(), 2)
        self.assertEqual(JSONRequiredModel.objects.filter(json=None).count(), 1)

    def test_isnull_lookup(self):
        JSONNotRequiredModel.objects.create(json=None)
        JSONNotRequiredModel.objects.create(json=100)
        self.assertEqual(JSONNotRequiredModel.objects.count(), 2)
        self.assertEqual(JSONNotRequiredModel.objects.filter(json__isnull=True).count(), 1)

        # isnull is incompatible with non-nullable fields, as the value is
        # serialized as '"null"'.
        JSONRequiredModel.objects.create(json=None)
        JSONRequiredModel.objects.create(json=100)
        self.assertEqual(JSONRequiredModel.objects.count(), 2)
        self.assertEqual(JSONRequiredModel.objects.filter(json__isnull=True).count(), 0)

    def test_regex_lookup(self):
        JSONModel.objects.create(json={'boom': 'town'})
        JSONModel.objects.create(json={'move': 'town'})
        JSONModel.objects.create(json={'save': 'town'})

        self.assertEqual(JSONModel.objects.count(), 3)
        self.assertEqual(JSONModel.objects.filter(json__regex=r'boom').count(), 1)
        self.assertEqual(JSONModel.objects.filter(json__regex=r'town').count(), 3)
