from django.conf.urls import patterns, include, url
from django.contrib import admin
from boom import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'boom.views.search', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'search/$',views.search),
    url(r'^admin/', include(admin.site.urls)),

    url(r'boom/(?P<query>.*)$',views.search)
)
