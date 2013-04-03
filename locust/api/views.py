from django.shortcuts import render_to_response
from locust.api.models import OpenCivicID

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings

import datetime as dt
import urllib2
import json


def render_api_response(obj):
    return HttpResponse(json.dumps(obj))


def query_pentagon(lat, lon):
    url = settings.PENTAGON_URL
    url += "/boundaries/?contains={lat},{lon}".format(**locals())
    return [x['external_id'] for x in
            json.load(urllib2.urlopen(url))['objects']]


def index(request):
    return render_to_response("locust/api/index.html", {})


def query_space_time(request):
    lat, lon = [request.GET[x] for x in ['lat', 'lon']]
    date = request.GET["date"] if "date" in request.GET else None
    if date:
        date = dt.datetime.strptime(date, "%Y-%m-%d")


    ids = query_pentagon(lat, lon)
    query = {"id__in": ids}
    if date:
        query["start__lt"] = date
        query["end__gt"] = date
    else:
        query["end"] = None

    objs = OpenCivicID.objects.filter(**query)
    return render_api_response({
        "response": [x.external_id for x in objs],
        "_original_response": ids,
        "meta": {
            "status": "ok",
            "_pentagon_responses": len(ids),
            "_locust_responses": len(objs)
        }
    })
