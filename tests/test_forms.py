from django import forms
from django.test import TestCase

from .models import JSONNotRequiredModel


class JSONModelFormTest(TestCase):
    def setUp(self):
        class JSONNotRequiredForm(forms.ModelForm):
            class Meta:
                model = JSONNotRequiredModel
                fields = '__all__'

        self.form_class = JSONNotRequiredForm

    def test_blank_form(self):
        form = self.form_class(data={'json': ''})
        self.assertFalse(form.has_changed())

    def test_form_with_data(self):
        form = self.form_class(data={'json': '{}'})
        self.assertTrue(form.has_changed())

    def test_form_save(self):
        form = self.form_class(data={'json': ''})
        form.save()

    def test_save_values(self):
        values = [
            # (type, form input, db value)
            ('object', '{"a": "b"}', {'a': 'b'}),
            ('array', '[1, 2]', [1, 2]),
            ('string', '"test"', 'test'),
            ('float', '1.2', 1.2),
            ('int', '1234', 1234),
            ('bool', 'true', True),
            ('null', 'null', None),
        ]

        for vtype, form_input, db_value in values:
            with self.subTest(type=vtype, input=form_input, db=db_value):
                form = self.form_class(data={'json': form_input})
                self.assertTrue(form.is_valid(), msg=form.errors)

                instance = form.save()
                self.assertEqual(instance.json, db_value)

    def test_render_initial_values(self):
        values = [
            # (type, db value, form output)
            ('object', {'a': 'b'}, '{\n    "a": "b"\n}'),
            ('array', [1, 2], "[\n    1,\n    2\n]"),
            ('string', 'test', '"test"'),
            ('float', 1.2, '1.2'),
            ('int', 1234, '1234'),
            ('bool', True, 'true'),
            ('null', None, 'null'),
        ]

        for vtype, db_value, form_output in values:
            with self.subTest(type=vtype, db=db_value, output=form_output):
                instance = JSONNotRequiredModel.objects.create(json=db_value)

                form = self.form_class(instance=instance)
                self.assertEqual(form['json'].value(), form_output)

    def test_render_bound_values(self):
        values = [
            # (type, db value, form input, form output)
            ('object', '{"a": "b"}', '{\n    "a": "b"\n}'),
            ('array', '[1, 2]', "[\n    1,\n    2\n]"),
            ('string', '"test"', '"test"'),
            ('float', '1.2', '1.2'),
            ('int', '1234', '1234'),
            ('bool', 'true', 'true'),
            ('null', 'null', 'null'),
        ]

        for vtype, form_input, form_output in values:
            with self.subTest(type=vtype, input=form_input, output=form_output):
                form = self.form_class(data={'json': form_input})
                self.assertEqual(form['json'].value(), form_output)

    def test_render_indent(self):
        form = self.form_class(initial={'json': {'a': 'b'}})
        self.assertEqual(form['json'].value(), '{\n    "a": "b"\n}')

    def test_render_unicode(self):
        form = self.form_class(initial={'json': '✨'})
        self.assertEqual(form['json'].value(), '"✨"')

    def test_invalid_value(self):
        form = self.form_class(data={'json': 'foo'})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'json': ['"foo" value must be valid JSON.'],
        })
        self.assertEqual(form['json'].value(), 'foo')

    def test_disabled_field(self):
        instance = JSONNotRequiredModel.objects.create(json=100)

        form = self.form_class(data={'json': '{"foo": "bar"}'}, instance=instance)
        form.fields['json'].disabled = True

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, {'json': 100})

        # rendered value
        self.assertEqual(form['json'].value(), '100')

    def test_initial_data_has_changed(self):
        instance = JSONNotRequiredModel.objects.create(json=[1, 2])

        form = self.form_class(data={'json': '[1, 2]'}, instance=instance)
        self.assertFalse(form.has_changed())

        form = self.form_class(data={'json': '[3, 4]'}, instance=instance)
        self.assertTrue(form.has_changed())


class NonJSONFieldModelFormTest(TestCase):
    """Test model form behavior when field class has been overridden."""

    def setUp(self):
        class JSONNotRequiredForm(forms.ModelForm):
            class Meta:
                model = JSONNotRequiredModel
                fields = ['json']
                field_classes = {
                    'json': forms.CharField,
                }

        self.form_class = JSONNotRequiredForm

    def test_field_type(self):
        form = self.form_class()
        field = form.fields['json']

        self.assertIsInstance(field, forms.CharField)

    def test_field_kwargs(self):
        form = self.form_class()
        field = form.fields['json']

        self.assertFalse(hasattr(field, 'dump_kwargs'))
        self.assertFalse(hasattr(field, 'load_kwargs'))

    def test_no_indent(self):
        # Because we're using a regular CharField, the value is not parsed and
        # rerendered with indentation. Compare with `test_render_bound_values`.
        form = self.form_class(data={'json': '{"a": "b"}'})
        self.assertEqual(form['json'].value(), '{"a": "b"}')
