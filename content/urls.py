from django.conf             import settings
from django.conf.urls        import url
from django.conf.urls.static import static
from .                       import views

################################################################################
# URL patterns for content
################################################################################
# (?P<question_id>[0-9]+)/
urlpatterns += [
    url(r'^$',                       views.index,             name='index'),
    url(r'^profile$',                views.profile,           name='profile'),
    url(r'^pie$',                    views.pie,               name='piechart'),
    url(r'^line$',                   views.demo_linechart,    name='linechart'),
    url(r'^scatter$',                views.demo_scatterchart, name='scatterchart'),
    url(r'^autograde/(\d+)/(\d+)$', views.autograde,         name='autograde'),
    url(r'^item/(\d+)$',            views.item_detail,       name='detail'),
    url(r'^item$',                  views.items,             name='list'),
    url(r'^table$',                 views.question_list,     name='question_list'),
    url(r'^question/(\d+)/(\d+)$',  views.assess_question_detail, name='detail'),
    url(r'^question/(\d+)$',        views.question_detail,   name='detail'),
    url(r'^question$',              views.questions,         name='list'),
    url(r'^assessment/(\d+)$',      views.assessment_detail, name='detail'),
    url(r'^assessment/(\d+)/worksheet$', views.assessment_worksheet, name='worksheet'),
    url(r'^assessment$',            views.assessments,       name='list'),
    url(r'^lecture/(\d+)$',         views.lecture_detail,    name='detail'),
    url(r'^lecture$',               views.lectures,          name='list'),
    url(r'^code/(\d+)$',            views.code_detail,       name='detail'),
    url(r'^login$',                 views.login_page,        name='login'),
    url(r'^auth$',                  views.auth,              name='auth'),
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
