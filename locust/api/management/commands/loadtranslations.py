from django.core.management.base import BaseCommand, CommandError
from locust.api.models import OpenCivicID

import datetime as dt
import os


def parse_date(string):
    fmts = [
        "%Y-%m-%d",  # YYY-MM-DD
        "%Y-%m",  #    YYY-MM
        "%Y",  #       YYY
    ]

    for fmt in fmts:
        try:
            obj = dt.datetime.strptime(string, fmt)
        except ValueError:
            obj = None

        if obj:
            return obj
    return None


def itertsv(fpath):
    fd = open(fpath, 'r')
    headers = [x.strip() for x in next(fd).split("\t")]

    for line in fd:
        if line.startswith("#"):
            continue

        yield dict(zip(headers, [x.strip() for x in line.split("\t")]))


def update_db(path, place):
    for bits in itertsv(path):
        name = place['namer'](bits)
        external_id = bits['GEOID']

        try:
            obj = OpenCivicID.objects.get(external_id=external_id)
        except OpenCivicID.DoesNotExist:
            obj = OpenCivicID()

        obj.id = name
        obj.start = dt.datetime.now()  # XXX: Don't do this.
        obj.external_id = external_id

        print "Saving: %s" % (name)
        obj.save()


class Command(BaseCommand):
    help = 'Loads in tons of data'

    def handle(self, *args, **options):
        if not args:
            print "Hurm. I need a directory to look at. Not doing anything."
            return

        dirs = args
        for d in dirs:
            mod = __import__(d)
            for place in mod.PLACES:
                update_db(os.path.join(d, place), mod.PLACES[place])
