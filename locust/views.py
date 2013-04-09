from django.shortcuts import render_to_response
from .models import DivisionGeometry, Division
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


def query_pentagon_by_lat_lon(lat, lon):
    url = "/boundaries/?contains={lat},{lon}".format(**locals())
    return [x['name'] for x in query_pentagon(url)['objects']]


def query_pentagon(url):
    URL = settings.PENTAGON_URL
    URL += url
    return json.load(urllib2.urlopen(URL))


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
        "response": [query_pentagon(fmt.format(set_id=x.set_id,
            external_id=x.external_id)) for x in geoms],
        "meta": {
            "status": "ok",
            "division": {
                "id": obj.id,
                "country": obj.country
            }
        }
    })


def query_lookup(request, query):
    if "/" in query:
        queries = query.split("/")
    else:
        queries = [query]

    dbq = []
    for query in queries:
        if ":" not in query:
            raise Http404("Invalid query: %s" % (query))

        _type, value = query.split(":", 1)
        q = Division.create_query(_type, value)
        dbq.append(q)

    objs = Division.objects.filter(*dbq)

    return render_api_response({
        "response": [x.id for x in objs],
        "meta": {"status": "ok"}
    })
