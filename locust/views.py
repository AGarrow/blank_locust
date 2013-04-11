from django.shortcuts import render_to_response
from .models import DivisionGeometry, Division, TemporalSet
from boundaries.models import Boundary
from django.http import Http404

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q

import datetime as dt
import urllib2
import json


def render_api_response(obj):
    return HttpResponse(json.dumps(obj))


def query_pentagon_by_lat_lon(lat, lon, sets=None):
    url = "/boundaries/?contains={lat},{lon}".format(**locals())
    if sets:
        url += "&sets={sets}".format(sets=",".join(s.slug for s in sets))

    return [x['name'] for x in query_pentagon(url)['objects']]


def query_pentagon(url):
    URL = settings.PENTAGON_URL
    URL += url
    return json.load(urllib2.urlopen(URL))


def query_space_time(request):
    lat, lon = [request.GET[x] for x in ['lat', 'lon']]
    date = request.GET["date"] if "date" in request.GET else None
    if date:
        date = dt.datetime.strptime(date, "%Y-%m-%d")
    else:
        date = dt.datetime.now()

    valid_sets = TemporalSet.objects.filter(
        Q(start__lt=date), Q(end__gte=date) | Q(end=None))

    sets = [x.boundary_set for x in valid_sets]

    point = 'POINT(%s %s)' % (lon, lat)

    bounds = Boundary.objects.filter(shape__contains=point, set__in=sets)
    geoms = DivisionGeometry.objects.filter(boundary__in=x)

    return render_api_response({
        "response": [x.division.id for x in geoms],
#        "_original_response": ids,
        "meta": {
            "status": "ok",
#            "_pentagon_responses": len(ids),
#            "_locust_responses": len(objs)
        }
    })


def query_by_ocd_id(request, ocdid):
    obj = Division.objects.get(id=ocdid)
    geoms = DivisionGeometry.objects.filter(division=obj)
    fmt = "/boundaries/{set_id}/{external_id}/"

    response = {
        "division": {"id": obj.id, "country": obj.country,
                     "display_name": obj.display_name}
    }
    response['children'] = [{"id": d.id, "display_name": d.display_name}
                            for d in Division.objects.children_of(ocdid)]
    response['boundaries'] = [query_pentagon(
        fmt.format(set_id=x.set_id, external_id=x.external_id)) for x in geoms]

    return render_api_response({
        "response": response,
    })
