"""
	Copy this file to localsettings.py to make local overrides.
	BEWARE to always import defaultsettings as well if activate this file.
"""

from .defaultsettings import *

DATABASES['default'] = {
	'ENGINE': 'django.db.backends.postgresql_psycopg2',
	'NAME': 'videos',  # database name
	'USER': 'videos',
	'PASSWORD': 'v3r7s3cr3t',
	'HOST': 'localhost',
	'PORT': '5432',
}
