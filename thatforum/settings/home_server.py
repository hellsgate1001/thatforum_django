from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.contrib.sqlite3',
        'NAME': 'db_thatforum.sqlite3',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
    }
}
