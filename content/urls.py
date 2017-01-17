from django.conf             import settings
from django.conf.urls        import url
from django.conf.urls.static import static
from .                       import views

################################################################################
# URL patterns for content
################################################################################
# (?P<item_id>[0-9]+)/
urlpatterns += [
    url(r'^$',                       views.index,             name='index'),
    url(r'^profile$',                views.profile,           name='profile'),

    #url(r'^pie$',                    views.pie,               name='piechart'),
    #url(r'^line$',                   views.demo_linechart,    name='linechart'),
    #url(r'^scatter$',                views.demo_scatterchart, name='scatterchart'),

    url(r'^autograde/(\d+)/(\d+)$',  views.autograde,         name='autograde'),

    url(r'^item/(\d+)$',             views.item,            name='detail'),
    url(r'^items$',                  views.items,           name='list'),
    url(r'^set/(\d+)$',              views.set,             name='detail'),
    url(r'^set$',                    views.sets,            name='detail'),

    url(r'^login$',                  views.login_page,        name='login'),
    url(r'^auth$',                   views.auth,              name='auth'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
################################################################################

################################################################################
# Static content
################################################################################
if settings.DEBUG:
    urlpatterns += ['', 
                              (r'media/(?P<path>.*)$', 
                               'django.views.static.serve', 
                               {'document_root': settings.MEDIA_ROOT}
                              )
                   ]
################################################################################
