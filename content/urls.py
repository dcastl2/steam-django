from django.conf             import settings
from django.conf.urls        import url, patterns
from django.conf.urls.static import static
from content                 import views

################################################################################
# URL patterns for content
################################################################################
# (?P<question_id>[0-9]+)/
urlpatterns = patterns(
    url(r'^$',                 views.index,             name='index'),
    url(r'^autograde/(\d+)-(\d+)$', views.autograde,         name='autograde'),
    url(r'^item/(\d+)$',       views.item_detail,       name='detail'),
    url(r'^items$',            views.items,             name='list'),
    url(r'^question/(\d+)$',   views.question_detail,   name='detail'),
    url(r'^questions$',        views.questions,         name='list'),
    url(r'^assessment/(\d+)$', views.assessment_detail, name='detail'),
    url(r'^assessments$',      views.assessments,       name='list'),
    url(r'^lecture/(\d+)$',    views.lecture_detail,    name='detail'),
    url(r'^lectures$',         views.lectures,          name='list'),
    url(r'^code/(\d+)$',       views.code_detail,       name='detail'),
    url(r'^login$',            views.login_page,        name='login'),
    url(r'^auth$',             views.auth,              name='auth'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
################################################################################

################################################################################
# Static content
################################################################################
if settings.DEBUG:
    urlpatterns += patterns('', 
                              (r'media/(?P<path>.*)$', 
                               'django.views.static.serve', 
                               {'document_root': settings.MEDIA_ROOT}
                              )
                           )
################################################################################
