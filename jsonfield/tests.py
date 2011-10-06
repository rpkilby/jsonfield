from django.db import models
from django.test import TestCase
from django.utils import simplejson as json

from fields import JSONField


class JsonModel(models.Model):
    json = JSONField()


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return {
                '__complex__': True,
                'real': obj.real,
                'imag': obj.imag,
            }

        return json.JSONEncoder.default(self, obj)


def as_complex(dct):
    if '__complex__' in dct:
        return complex(dct['real'], dct['imag'])
    return dct


class JSONModelCustomEncoders(models.Model):
    # A JSON field that can store complex numbers
    json = JSONField(
        dump_kwargs={'cls': ComplexEncoder},
        load_kwargs={'object_hook': as_complex},
    )


class JSONFieldTest(TestCase):
    """JSONField Wrapper Tests"""

    def test_json_field_create(self):
        """Test saving a JSON object in our JSONField"""

        json_obj = {
            "item_1": "this is a json blah",
            "blergh": "hey, hey, hey"}

        obj = JsonModel.objects.create(json=json_obj)
        new_obj = JsonModel.objects.get(id=obj.id)

        self.failUnlessEqual(new_obj.json, json_obj)

    def test_json_field_modify(self):
        """Test modifying a JSON object in our JSONField"""

        json_obj_1 = {'a': 1, 'b': 2}
        json_obj_2 = {'a': 3, 'b': 4}

        obj = JsonModel.objects.create(json=json_obj_1)

        self.failUnlessEqual(obj.json, json_obj_1)

        obj.json = json_obj_2

        self.failUnlessEqual(obj.json, json_obj_2)

        obj.save()

        self.failUnlessEqual(obj.json, json_obj_2)

        self.assert_(obj)

    def test_json_field_load(self):
        """Test loading a JSON object from the DB"""

        json_obj_1 = {'a': 1, 'b': 2}

        obj = JsonModel.objects.create(json=json_obj_1)

        new_obj = JsonModel.objects.get(id=obj.id)

        self.failUnlessEqual(new_obj.json, json_obj_1)

    def test_json_list(self):
        """Test storing a JSON list"""

        json_obj = ["my", "list", "of", 1, "objs", {"hello": "there"}]

        obj = JsonModel.objects.create(json=json_obj)
        new_obj = JsonModel.objects.get(id=obj.id)
        self.failUnlessEqual(new_obj.json, json_obj)

    def test_empty_objects(self):
        """Test storing empty objects"""

        for json_obj in [{}, [], 0, '', False]:
            obj = JsonModel.objects.create(json=json_obj)
            new_obj = JsonModel.objects.get(id=obj.id)
            self.failUnlessEqual(json_obj, obj.json)
            self.failUnlessEqual(json_obj, new_obj.json)

    def test_custom_encoder(self):
        """Test encoder_cls and object_hook"""
        value = 1 + 3j  # A complex number

        obj = JSONModelCustomEncoders.objects.create(json=value)
        new_obj = JSONModelCustomEncoders.objects.get(pk=obj.pk)
        self.failUnlessEqual(value, new_obj.json)
