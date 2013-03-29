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


def itercsv(fpath):
    for line in open(fpath, 'r'):
        if line.startswith("#"):
            continue

        yield [x.strip() for x in line.split(",")]


def update_db(path):
    for internal_id, _id, start, end, description in itercsv(path):
        start, end = (parse_date(x) for x in (start, end))

        try:
            obj = OpenCivicID.objects.get(internal_id=internal_id)
        except OpenCivicID.DoesNotExist:
            obj = OpenCivicID()

        obj.id = _id
        obj.start = start
        obj.end = end
        # obj.description = description
        obj.internal_id = internal_id

        print "Saving: {_id}".format(**locals())
        obj.save()


class Command(BaseCommand):
    help = 'Loads in tons of data'

    def handle(self, *args, **options):
        if not args:
            print "Hurm. I need a directory to look at. Not doing anything."
            return

        for path in args:
            for _file in os.walk(path):
                root, folders, files = _file
                for _fname in filter(lambda x: x.endswith(".csv"), files):
                    path = "/".join([root, _fname])
                    update_db(path)
