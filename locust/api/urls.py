from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'locust.api.views.index', name='index'),
    url(r'^query/$', 'locust.api.views.query_space_time', name='query'),
)
