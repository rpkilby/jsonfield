import json
import warnings

from django.test import TestCase

from jsonfield.fields import JSONField

from .models import JSONModel


class TestFieldAPIMethods(TestCase):
    def test_get_db_prep_value_method_with_null(self):
        json_field_instance = JSONField(null=True)
        value = {'a': 1}
        prepared_value = json_field_instance.get_db_prep_value(
            value, connection=None, prepared=False)
        self.assertIsInstance(prepared_value, str)
        self.assertDictEqual(value, json.loads(prepared_value))
        self.assertIs(json_field_instance.get_db_prep_value(
            None, connection=None, prepared=True), None)
        self.assertIs(json_field_instance.get_db_prep_value(
            None, connection=None, prepared=False), None)

    def test_get_db_prep_value_method_with_not_null(self):
        json_field_instance = JSONField(null=False)
        value = {'a': 1}
        prepared_value = json_field_instance.get_db_prep_value(
            value, connection=None, prepared=False)
        self.assertIsInstance(prepared_value, str)
        self.assertDictEqual(value, json.loads(prepared_value))
        self.assertIs(json_field_instance.get_db_prep_value(
            None, connection=None, prepared=True), None)
        self.assertEqual(json_field_instance.get_db_prep_value(
            None, connection=None, prepared=False), 'null')

    def test_get_db_prep_value_method_skips_prepared_values(self):
        json_field_instance = JSONField(null=False)
        value = {'a': 1}
        prepared_value = json_field_instance.get_db_prep_value(
            value, connection=None, prepared=True)
        self.assertIs(prepared_value, value)

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

    def test_from_db_value_deprecation_warning(self):
        # Compatibility for Django 1.11 and earlier
        # Django 2.0+ drops the `context` argument
        JSONModel.objects.create(json='{}')

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            JSONModel.objects.get()

        self.assertEqual(w, [])
