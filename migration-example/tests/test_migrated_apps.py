from django.test import TestCase

from alterfield.models import AlterFieldModel
from datamigration.models import DataMigrationModel


class Testcases:
    def test_numeric(self):
        self.assertEqual(self.model.objects.get(pk=1).data, 1)

    def test_string(self):
        self.assertEqual(self.model.objects.get(pk=2).data, "foobar")

    def test_object(self):
        self.assertEqual(self.model.objects.get(pk=3).data, {"foo": "bar"})



class AlterFieldTests(Testcases, TestCase):
    model = AlterFieldModel



class DataMigrationTests(Testcases, TestCase):
    model = DataMigrationModel
