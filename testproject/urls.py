from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from .views import raise_error, ClassBasedView

urlpatterns = patterns('',
    url(r'^error500/$', raise_error),
    url(r'^class_based/$', ClassBasedView.as_view()),                   
    # Examples:
    # url(r'^$', 'testproject.views.home', name='home'),
    # url(r'^testproject/', include('testproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
                           
    url(r'^admin/', include(admin.site.urls)),
)
