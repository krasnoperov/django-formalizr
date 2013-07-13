#!/usr/bin/env python
import sys

from django.conf import settings

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=(
        'formalizr',
        'formalizr.tests',
    ),
    SITE_ID=1
)

from django.test.utils import get_runner


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests([])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()

