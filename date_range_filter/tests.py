import datetime
from copy import deepcopy as copy

import six
from django.test import TestCase, override_settings
from django.utils import timezone

import pytz

from . import DateRangeFilter
from .filter import DateRangeForm

if six.PY3:
    from unittest.mock import MagicMock
else:
    from mock import MagicMock


class TestDateRangeForm(TestCase):
    def setUp(self):
        self.form = DateRangeForm()
        self.form.cleaned_data = {
            'date_start': datetime.date(2016, 1, 15),
            'date_end': datetime.date(2016, 2, 10),
        }

    @classmethod
    def setUpClass(self):
        super(TestDateRangeForm, self).setUpClass()
        self.tz = pytz.timezone('Europe/Moscow')
        timezone.activate(self.tz)

    def test_field_auto_naming(self):
        form = DateRangeForm()
        self.assertIsNotNone(form.fields['date_start'])
        self.assertIsNotNone(form.fields['date_end'])

    def test_field_custom_naming(self):
        form = DateRangeForm(field_name='testing')
        self.assertIsNotNone(form.fields['testing_start'])
        self.assertIsNotNone(form.fields['testing_end'])

    def test_invalid_date(self):
        self.assertIsNone(self.form.start_date())  # form is not valid by default
        self.assertIsNone(self.form.end_date())

    def test_start_date(self):
        self.form.is_valid = MagicMock(return_value=True)
        self.assertEqual(self.form.start_date(), timezone.make_aware(datetime.datetime(2016, 1, 15)))

    def test_end_time(self):
        self.form.is_valid = MagicMock(return_value=True)
        self.assertEqual(self.form.end_date(), timezone.make_aware(datetime.datetime(2016, 2, 10, 23, 59, 59, 999999)))

    @override_settings(USE_TZ=False)
    def test_without_timezone(self):
        self.form.is_valid = MagicMock(return_value=True)
        self.assertEqual(self.form.start_date(), datetime.datetime(2016, 1, 15))
        self.assertEqual(self.form.end_date(), datetime.datetime(2016, 2, 10, 23, 59, 59, 999999))


class TestDateRangeFilter(TestCase):
    """
    All tests in this suite are static to bypass mocking compicated django.admin.filter.FieldListFilter
    """
    def setUp(self):
        self.cls = copy(DateRangeFilter)
        self.cls.field_path = 'testing'
        self.instance = self.cls(
            field=None,
            request=None,
            params=[],
            model=None,
            model_admin=None,
            field_path=self.cls.field_path,
        )
        self.instance.field_path = self.cls.field_path

    def test_expected_parameters(self):
        params = self.cls.expected_parameters(self.instance)
        self.assertTupleEqual(params, ('testing_start', 'testing_end'))

    def test_filter_arguments(self):
        args = self.cls._DateRangeFilter__get_filterargs(self.instance, 'spam', 'eggs')
        self.assertDictEqual(args, {
            'testing__gte': 'spam',
            'testing__lte': 'eggs',
        })

    def test_queryset(self):
        fake_form = MagicMock()
        fake_form.cleaned_data = {
            'date_start': datetime.date(2016, 1, 15),
            'date_end': datetime.date(2016, 2, 10),
        }
        fake_form.is_valid = MagicMock(return_value=True)

        self.cls.get_form = MagicMock(return_value=fake_form)

        queryset = MagicMock()
        queryset.filter = MagicMock()

        self.cls._DateRangeFilter__get_filterargs = MagicMock()

        self.cls.queryset(self.instance, request='request-placeholder', queryset=queryset)

        self.assertEqual(queryset.filter.call_count, 1)
