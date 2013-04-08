from ...models import Division, DivisionGeometry
from django.core.management.base import BaseCommand, CommandError

import datetime as dt
import urllib2
import csv


class Command(BaseCommand):
    help = 'Loads in geoid mapping things'

    def handle(self, *args, **options):
        args = list(args)
        set_id = args.pop(0)

        for arg in args:
            print arg, '...',
            count = 0
            for ocd_id, geo_id in csv.reader(urllib2.urlopen(arg)):
                division = Division.objects.get(id=ocd_id)
                try:
                    geom = DivisionGeometry.objects.get(external_id=geo_id)
                except DivisionGeometry.DoesNotExist:
                    geom = DivisionGeometry(division=division)

                if geom.division.id != division.id:
                    geom.delete()

                geom.external_id = geo_id
                geom.division = division
                geom.set_id = set_id
                geom.start = dt.datetime.now()
                geom.save()
                count += 1

            print count, 'objects'
