from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'cms.views.index'),
    url(r'^changeTerm/', 'cms.views.get_json'),
)

urlpatterns += staticfiles_urlpatterns()