from django.core.management.base import BaseCommand, CommandError
from locust.api.models import OpenCivicID

import datetime as dt
import os


def open_civic_namer(block, encoding='latin1'):
    # {'INTPTLAT': '32.536382', 'NAME': 'Autauga County', 'INTPTLONG': '-86.644490', 'USPS': 'AL', 'AWATER_SQMI': '9.952', 'AWATER': '25775735', 'ANSICODE': '00161526', 'HU10': '22135', 'POP10': '54571', 'ALAND_SQMI': '594.436', 'GEOID': '01001', 'ALAND': '1539582278'}
    name = block['NAME'].lower().replace(" ", "-").decode(encoding)
    state_name = block['USPS']
    return "ocd:place/%s/place/place:%s" % (state_name, name)




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


def update_db(path):
    for bits in itertsv(path):
        name = open_civic_namer(bits)
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

        for path in args:
            for _file in os.walk(path):
                root, folders, files = _file
                for _fname in filter(lambda x: x.endswith(".txt"), files):
                    path = "/".join([root, _fname])
                    update_db(path)
