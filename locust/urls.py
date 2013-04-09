from django.conf.urls import patterns, include, url

urlpatterns = patterns('locust.views',
    url(r'^$', 'index', name='index'),
    url(r'^query/$', 'query_space_time', name='query'),
    url(r'^get/(?P<ocdid>.*)/$', 'query_by_ocd_id', name='get'),
    url(r'^lookup/(?P<query>.*)/$', 'query_lookup', name='get'),
)
