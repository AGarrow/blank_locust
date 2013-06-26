from django.conf.urls import patterns, include, url

(r'', include('boundaries.urls')),

urlpatterns = patterns('locust.views',
    url(r'^$', 'query_space_time', name='query'),
    url(r'^(?P<ocdid>.*)/$', 'query_by_ocd_id', name='get'),
)
