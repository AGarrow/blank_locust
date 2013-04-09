from django.conf.urls import patterns, include, url

urlpatterns = patterns('locust.views',
    url(r'^$', 'index', name='index'),
    url(r'^query-lat-lon/$', 'query_space_time', name='query'),
    url(r'^get/(?P<ocdid>.*)/$', 'query_by_ocd_id', name='get'),
    url(r'^search/(?P<query>.*)/$', 'query_lookup', name='get'),
)
