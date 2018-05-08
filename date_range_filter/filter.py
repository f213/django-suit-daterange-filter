from datetime import datetime, time

import six
from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import pgettext
from suit.widgets import SuitDateWidget


class DateRangeForm(forms.Form):

    def __init__(self, *args, **kwargs):
        """
        Automaticaly generate form fields with dynamic names based on the filtering field name
        """
        self.field_name = kwargs.pop('field_name', 'date')
        super(DateRangeForm, self).__init__(*args, **kwargs)

        self.fields['%s_start' % self.field_name] = forms.DateField(
            widget=SuitDateWidget, label=pgettext('date', 'From'), required=False)
        self.fields['%s_end' % self.field_name] = forms.DateField(
            widget=SuitDateWidget, label=pgettext('date', 'To'), required=False)

    def start_date(self):
        if self.is_valid():
            start = self.cleaned_data.get('%s_start' % self.field_name)
            if start:
                start = datetime.combine(start, time.min)

                if settings.USE_TZ:
                    return timezone.make_aware(start)

            return start

    def end_date(self):
        if self.is_valid():
            end = self.cleaned_data.get('%s_end' % self.field_name)
            if end:
                end = datetime.combine(end, time.max)

                if settings.USE_TZ:
                    return timezone.make_aware(end)

            return end

    class Media:
        css = {
            'all': ('date_range_filter.css',),
        }


class DateRangeFilter(admin.FieldListFilter):
    template = 'admin/date_range_filter.html'

    def expected_parameters(self):
        return ('%s_start' % self.field_path, '%s_end' % self.field_path)

    def choices(self, cl):
        return [{
            'query_string': [] if six.PY3 else '',
        }]

    def get_form(self, request):
        return DateRangeForm(data=request.GET, field_name=self.field_path)

    def queryset(self, request, queryset):
        form = self.get_form(request)

        """
        That's the trick - we create self.form when django tries to get our queryset.
        This allowes to create unbount and bound form in the single place.
        """
        self.form = form

        start_date = form.start_date()
        end_date = form.end_date()

        if form.is_valid() and (start_date or end_date):
            args = self.__get_filterargs(
                start=start_date,
                end=end_date,
            )
            return queryset.filter(**args)

    def __get_filterargs(self, start, end):
        filterargs = {}
        if start:
            filterargs[self.field_path + '__gte'] = start
        if end:
            filterargs[self.field_path + '__lte'] = end
        return filterargs
