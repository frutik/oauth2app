from django.conf.urls.defaults import *

urlpatterns = patterns('vipsatis.oauth2authorizer.views',
    url(r'^token/$', 'token', name="oauth2app-contrib-authoriser-token"),
)
