from django.conf.urls import patterns, include, url
from django.contrib import admin
from boom.views import search,home

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'boom.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'boom/$',home),
    url(r'boom/(?P<query>.*)$',search)
)
