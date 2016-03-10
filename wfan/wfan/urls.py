from django.conf.urls import patterns, url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^cms/', include('cms.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )
