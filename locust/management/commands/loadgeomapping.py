from ...models import Division, DivisionGeometry
from django.core.management.base import BaseCommand, CommandError

import datetime as dt
import urllib2
import csv

TYPE_SET_MAPPER = {
    "county": "county",
    "place": "place",
    "parish": "county",
    "borough": "county",
}


class Command(BaseCommand):
    help = 'Loads in geoid mapping things'

    def handle(self, *args, **options):
        args = list(args)
        set_year = args.pop(0)

        if args == []:
            raise Exception("Need URL to grab. - did you give me a set year ID?")

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

                _type, short_id = [
                    x.split(":", 1) for x in division.id.split("/")[1:]
                ][-1]
                set_id = "%s-%s" % (TYPE_SET_MAPPER[_type], set_year)

                geom.external_id = geo_id
                geom.division = division
                geom.set_id = set_id
                geom.start = dt.datetime.now()
                geom.save()
                count += 1

            print count, 'objects'
