#!/usr/bin/env python

import django
import nose
from django.conf import settings

settings.configure(
    USE_TZ=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'testdb.sqlite3',
        },
    },
)

django.setup()

nose.main()
