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


def query_pentagon(url):
    URL = settings.PENTAGON_URL
    URL += url
    return json.load(urllib2.urlopen(URL))


def query_space_time(request):
    lat, lon = [request.GET[x] for x in ['lat', 'lon']]

    date = request.GET.get('date')
    if date:
        date = dt.datetime.strptime(date, "%Y-%m-%d")
    else:
        date = dt.datetime.now()

    point = 'POINT(%s %s)' % (lon, lat)

    divisions = Division.objects.filter(
        Q(geometries__temporal_set__end__gte=date) |
        Q(geometries__temporal_set__end=None),
        geometries__temporal_set__start__lte=date,
        geometries__boundary__shape__contains=point,
    ).values_list('id', flat=True)

    return render_api_response({ "response": list(divisions) })


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
    response['geometries'] = [
        {'start': dg.temporal_set.start.strftime('%Y-%m-%d'),
         'end': dg.temporal_set.end.strftime('%Y-%m-%d') if dg.temporal_set.end else None,
         'boundary': dg.boundary.as_dict()
        } for dg in obj.geometries.all()]

    return render_api_response({
        "response": response,
    })
