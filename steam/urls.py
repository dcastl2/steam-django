from django.conf.urls import url, patterns, include
from django.contrib   import admin

################################################################################
# URL patterns for STEAM
################################################################################
urlpatterns = patterns(
    url(r'^', include('content.urls', namespace="content")),
    url(r'^', include('content.urls', namespace="content")),
    url(r'^admin/',   include(admin.site.urls)),
)
################################################################################
