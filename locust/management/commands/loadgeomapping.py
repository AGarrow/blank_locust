import csv
import urllib2

from django.core.management.base import BaseCommand, CommandError
from ...models import Division


class Command(BaseCommand):
    help = 'Loads in geoid mapping things'

    def handle(self, *args, **options):
        for arg in args:
            # load in mappings to geoids here, create DivisionGeometry
            # objects.
            pass
