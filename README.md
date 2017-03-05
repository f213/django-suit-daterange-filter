# Date range filter for django-admin

[![Build Status](https://travis-ci.org/f213/django-suit-daterange-filter.svg?branch=master)](https://travis-ci.org/f213/django-suit-daterange-filter)
[![PyPI version](https://badge.fury.io/py/django-suit-daterange-filter.svg)](https://badge.fury.io/py/django-suit-daterange-filter)

Yet another filter for Django admin interface, adding possibility to lookup by date range. The filter is only compatible with [django-suit](https://github.com/darklow/django-suit) (does anyone use ugly stock admin now?)

Key features:

* Support both DateField and DateTimeField
* User timezone support
* Simplest ever (< 128 SLOC)
* Well tested

Only python3 is supported.

## Installation

```sh
pip install django-suit-daterange-filter
```

Then add to the `settings.INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    'date_range_filter',
)
```

## Usage:
```python

from date_range_filter import DateRangeFilter

class EggAdmin(admin.ModelAdmin):
  list_filters = (
    'is_spam',
    'egg_count',
    ('timestamp', DateRangeFilter),
  )

```

## Issues:

If you have some JS errors about gettext, you should include django's built in i18n javascript, like this:
```python

class EggAdmin(admin.ModelAdmin):
  ...
  class Media:
    js = ['/admin/jsi18n/']
```

This module is heavily inspired by [django-daterange-filter](https://github.com/tzulberti/django-datefilterspec).
