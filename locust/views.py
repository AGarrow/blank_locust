from django.shortcuts import render_to_response
from .models import DivisionGeometry, Division

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q

import datetime as dt
import urllib2
import json


def render_api_response(obj):
    return HttpResponse(json.dumps(obj))


def query_pentagon_by_lat_lon(lat, lon):
    url = "/boundaries/?contains={lat},{lon}".format(**locals())
    return query_pentagon(url)


def query_pentagon(url):
    URL = settings.PENTAGON_URL
    URL += url
    return [x['name'] for x in json.load(urllib2.urlopen(URL))['objects']]


def index(request):
    return render_to_response("locust/api/index.html", {})


def query_space_time(request):
    lat, lon = [request.GET[x] for x in ['lat', 'lon']]
    date = request.GET["date"] if "date" in request.GET else None
    if date:
        date = dt.datetime.strptime(date, "%Y-%m-%d")
    else:
        date = dt.datetime.now()


    ids = query_pentagon_by_lat_lon(lat, lon)
    query = [Q(external_id__in=ids)]

    query.append(Q(start__lt=date))
    query.append(Q(end__gte=date) | Q(end=None))

    objs = DivisionGeometry.objects.filter(*query)
    return render_api_response({
        "response": list(set([x.division.id for x in objs])),
        "_original_response": ids,
        "meta": {
            "status": "ok",
            "_pentagon_responses": len(ids),
            "_locust_responses": len(objs)
        }
    })


def query_by_ocd_id(request, ocdid):
    obj = Division.objects.get(id=ocdid)
    geoms = DivisionGeometry.objects.filter(division=obj)
    fmt = "/boundaries/{set_id}/{external_id}/"

    return render_api_response({
        "response": [query_pentagon(fmt.format(**x)) for x in geoms],
        "meta": {"status": "ok"}
    })
