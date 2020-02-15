import json

from django.test import TestCase

from jsonfield.fields import JSONField
from jsonfield.json import JSONString


class TestFieldAPIMethods(TestCase):

    def test_get_prep_value_always_json_dumps_if_not_null(self):
        json_field_instance = JSONField(null=False)
        value = {'a': 1}
        prepared_value = json_field_instance.get_prep_value(value)
        self.assertIsInstance(prepared_value, str)
        self.assertDictEqual(value, json.loads(prepared_value))
        already_json = json.dumps(value)
        double_prepared_value = json_field_instance.get_prep_value(
            already_json)
        self.assertDictEqual(value,
                             json.loads(json.loads(double_prepared_value)))
        self.assertEqual(json_field_instance.get_prep_value(None), 'null')

    def test_get_prep_value_can_return_none_if_null(self):
        json_field_instance = JSONField(null=True)
        value = {'a': 1}
        prepared_value = json_field_instance.get_prep_value(value)
        self.assertIsInstance(prepared_value, str)
        self.assertDictEqual(value, json.loads(prepared_value))
        already_json = json.dumps(value)
        double_prepared_value = json_field_instance.get_prep_value(
            already_json)
        self.assertDictEqual(value,
                             json.loads(json.loads(double_prepared_value)))
        self.assertIs(json_field_instance.get_prep_value(None), None)

    def test_deconstruct_default_kwargs(self):
        field = JSONField()

        _, _, _, kwargs = field.deconstruct()

        self.assertNotIn('dump_kwargs', kwargs)
        self.assertNotIn('load_kwargs', kwargs)

    def test_deconstruct_non_default_kwargs(self):
        field = JSONField(
            dump_kwargs={'separators': (',', ':')},
            load_kwargs={'object_pairs_hook': dict},
        )

        _, _, _, kwargs = field.deconstruct()

        self.assertEqual(kwargs['dump_kwargs'], {'separators': (',', ':')})
        self.assertEqual(kwargs['load_kwargs'], {'object_pairs_hook': dict})

    def test_from_db_value_loaded_types(self):
        values = [
            # (label, db value, loaded type)
            ('object', '{"a": "b"}', dict),
            ('array', '[1, 2]', list),
            ('string', '"test"', JSONString),
            ('float', '1.2', float),
            ('int', '1234', int),
            ('bool', 'true', bool),
            ('null', 'null', type(None)),
        ]

        for label, db_value, inst_type in values:
            with self.subTest(type=label, db_value=db_value):
                value = JSONField().from_db_value(db_value, None, None)

                self.assertIsInstance(value, inst_type)
