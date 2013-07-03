locust
======

1.  add manage.py

    #!/usr/bin/env python
    import os
    import sys

    if __name__ == "__main__":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "locust.settings_local")

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)


2.  add requirements.txt

    Django
    -e git://github.com/rhymeswithcycle/represent-boundaries.git#egg=boundaries

3.  changed import line in loadgeomapping.py
  from
    from ...models import DivisionGeometry, TemporalSet
  to
    locust.models import DivisionGeometry, TemporalSet

4. add settings_local.py

the contents of this file may not <em> all </em> be necessary, but I've left them here until I determine what is.

        from os.path import abspath, dirname, join


        PROJECT_ROOT = abspath(join(dirname(__file__), '..'))

        DEBUG = True
        TEMPLATE_DEBUG = DEBUG

        SECRET_KEY = 'some_secret'

        ADMINS = (
            ('James Turk', 'jturk@sunlightfoundation.com'),
            ('Thom Neale', 'tneale@sunlightfoundation.com'),
            ('Thom Neale', 'twneale@gmail.com'),
            ('Paul Tagliamonte', 'paultag@sunlightfoundation.com'),
        )

        MANAGERS = ADMINS

        DATABASES = {
            'default': {
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'NAME': 'postgres',
                'USER': '',
                'PASSWORD': '',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }

        ALLOWED_HOSTS = []

        TIME_ZONE = 'America/Chicago'
        LANGUAGE_CODE = 'en-us'
        SITE_ID = 1
        USE_I18N = True
        USE_L10N = True
        USE_TZ = True
        MEDIA_ROOT = ''
        MEDIA_URL = ''

        STATIC_ROOT = join(PROJECT_ROOT, '..', 'collected_static')
        STATIC_URL = '/media/'

        STATICFILES_DIRS = (
            # Put strings here, like "/home/html/static" or "C:/www/django/static".
            # Always use forward slashes, even on Windows.
            # Don't forget to use absolute paths, not relative paths.
        )

        STATICFILES_FINDERS = (
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',

        )

        TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )

        TEMPLATE_CONTEXT_PROCESSORS = (
            'django.core.context_processors.request',
            'django.contrib.messages.context_processors.messages',
            'django.contrib.auth.context_processors.auth',
        )

        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            # Uncomment the next line for simple clickjacking protection:
            # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
        )

        ROOT_URLCONF = 'locust.urls'

        # WSGI_APPLICATION = 'anthropod.wsgi.application'

        TEMPLATE_DIRS = (
            # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
            # Always use forward slashes, even on Windows.
            # Don't forget to use absolute paths, not relative paths.
        )

        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.humanize',
            'boundaries'
        )

        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'filters': {
                'require_debug_false': {
                    '()': 'django.utils.log.RequireDebugFalse'
                }
            },
            'formatters': {
                },
            'handlers': {
                'mail_admins': {
                    'level': 'ERROR',
                    'filters': ['require_debug_false'],
                    'class': 'django.utils.log.AdminEmailHandler'
                },
            },
            'loggers': {
                'django.request': {
                    'handlers': ['mail_admins'],
                    'level': 'ERROR',
                    'propagate': True,
                },
            }
        }


        AUTHENTICATION_BACKENDS = (
            'sunlightauth.backends.SunlightBackend',
            'django.contrib.auth.backends.ModelBackend',
        )

        SUNLIGHT_AUTH_BASE_URL = 'http://login.sunlightfoundation.com/'
        # SUNLIGHT_AUTH_APP_ID = 'anthropod'
        SUNLIGHT_AUTH_APP_ID = 'openstates'
        #SUNLIGHT_AUTH_SECRET = 'set in local settings'
        SUNLIGHT_AUTH_SCOPE = []

        LOGIN_REDIRECT_URL = '/'
        LOGIN_URL = '/login/sunlight/'

        LOCKSMITH_REGISTRATION_URL = 'http://services.sunlightlabs.com/accounts/register/'

        TEST_RUNNER = 'django_nose.run_tests'



4. cloned [represent-boundaries](https://github.com/rhymeswithcycle/represent-boundaries), followed instructions, including adding line to url file (you can see 'boundaries' in INSTALLED APP in the settings_local.py file refered to above). This was all done in the same virtual environment as the locust directory (locust)

5.  set up postGIS

  GeoDjango is not compatible with PostGIS 2.0, so you must use PostGIS 1.5. PostGIS 1.5 is not compatible with PostgreSQL 9.2, so you must use PostgreSQL 9.0. If you already have PostGIS 2.0, run:

    brew unlink postgis
    Install PostGIS 1.5:

    brew tap homebrew/versions
    brew install postgis15
  Follow the PostgreSQL post-installation instructions:

    brew info postgresql9

6.  Create a PostGIS template database:

        createdb -h localhost -E UTF-8 postgres
        psql -h localhost -d postgres -f /usr/local/Cellar/postgis15/1.5.8/share/postgis/postgis.sql
        psql -h localhost -d postgres -f /usr/local/Cellar/postgis15/1.5.8/share/postgis/spatial_ref_sys.sql

    If either of the psql commands fail with could not access file "$libdir/postgis-1.5": No such file or directory:

    brew rm postgis15
    brew install postgis15
    Paste all the following commands as a single block:

    cat <<EOS | psql -h localhost -d postgres
    UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'postgres';
    GRANT ALL ON geometry_columns TO PUBLIC;
    GRANT ALL ON geography_columns TO PUBLIC;
    GRANT ALL ON spatial_ref_sys TO PUBLIC;
    VACUUM FREEZE;
    EOS

7. sync the database

        python manage.py syncdb

8. load shapefiles
    from within the cloned represent-boundaries directory

        python manage.py loadshapefiles

8. start the server

        python manage.py runserver



