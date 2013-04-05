import csv
import urllib2

from django.core.management.base import BaseCommand, CommandError
from ...models import Division


class Command(BaseCommand):
    help = 'Loads in tons of data'

    def handle(self, *args, **options):
        if not args:
            print 'must specify arguments'
            return

        for arg in args:
            print arg, '...',
            count = 0
            for name, ocd_id in csv.reader(urllib2.urlopen(arg)):
                pieces = ocd_id.split('/')
                if pieces.pop(0) != 'ocd-division':
                    raise Exception('ID must start with ocd-division/')
                country = pieces.pop(0)
                if not country.startswith('country:'):
                    raise Exception('Second part of ID must be country:')
                else:
                    country = country.strip('country:')
                n = 1
                args = {}
                for piece in pieces:
                    type_, id_ = piece.split(':')
                    args['subtype%s' % n] = type_
                    args['subid%s' % n] = id_
                    n += 1
                Division.objects.create(id=ocd_id, display_name=name,
                                        country=country, **args)
                count += 1
            print count, 'objects'
