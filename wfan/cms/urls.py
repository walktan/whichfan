from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'cms.views.index'),
    url(r'^surprise/', 'cms.views.get_json'),
)

urlpatterns += staticfiles_urlpatterns()