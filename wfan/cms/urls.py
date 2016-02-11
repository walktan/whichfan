from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('',
    url(r'^$', 'cms.views.index'),
    url(r'^surprise/', 'cms.views.for_ajax'),
    url(r'^graph/', 'cms.views.graph'),
)