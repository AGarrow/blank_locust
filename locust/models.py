from collections import OrderedDict
from django.db import models

DIVISION_ORDER = OrderedDict([
    ("subtype1", "subid1"),
    ("subtype2", "subid2"),
    ("subtype3", "subid3"),
    ("subtype4", "subid4"),
    ("subtype5", "subid5"),
    ("subtype6", "subid6"),
    ("subtype7", "subid7")
])


class Division(models.Model):
    id = models.CharField(max_length=300, primary_key=True)
    display_name = models.CharField(max_length=100)
    country = models.CharField(max_length=2)
    # up to 7 pieces of the id that are searchable
    subtype1 = models.CharField(max_length=50, null=True, blank=True)
    subid1 = models.CharField(max_length=100, null=True, blank=True)
    subtype2 = models.CharField(max_length=50, null=True, blank=True)
    subid2 = models.CharField(max_length=100, null=True, blank=True)
    subtype3 = models.CharField(max_length=50, null=True, blank=True)
    subid3 = models.CharField(max_length=100, null=True, blank=True)
    subtype4 = models.CharField(max_length=50, null=True, blank=True)
    subid4 = models.CharField(max_length=100, null=True, blank=True)
    subtype5 = models.CharField(max_length=50, null=True, blank=True)
    subid5 = models.CharField(max_length=100, null=True, blank=True)
    subtype6 = models.CharField(max_length=50, null=True, blank=True)
    subid6 = models.CharField(max_length=100, null=True, blank=True)
    subtype7 = models.CharField(max_length=50, null=True, blank=True)
    subid7 = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return '{0} ({1})'.format(self.display_name, self.id)

    @staticmethod
    def ocd_id_query(*compare):
        Q = models.Q
        compare = list(compare)

        ret = compare.pop(0)
        _type, value = ret
        if _type != "country":
            return None

        ret = [Q(country=value)]

        els = zip(compare, DIVISION_ORDER)
        for element in els:
            values, order = element
            subtype_id = DIVISION_ORDER[order]
            _type, value = values
            ret.append(Q(**{order: _type,
                            subtype_id: value}))

        return Division.objects.filter(*ret)


class DivisionGeometry(models.Model):
    division = models.ForeignKey(Division, related_name='geometries')
    # possibly refactor this to just point to a boundary object?
    external_id = models.CharField(max_length=128, unique=True)
    set_id = models.CharField(max_length=128)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.division, self.set_id,
                                        self.division_id)
