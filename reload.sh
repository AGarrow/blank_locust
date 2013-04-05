#!/bin/bash
set -e

python manage.py sqlclear locust | python manage.py dbshell
python manage.py syncdb
python manage.py loadtranslations translations
