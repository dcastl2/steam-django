from django.conf.urls import url, include
from django.contrib   import admin
from content import views

################################################################################
# URL patterns for STEAM
################################################################################

#print "*** admin.site.urls:",admin.site.urls

# When I uncomment the content urls, the admin interface successfully searches
# for the admin template. But when I include the content urls, the admin
# urls cannot be resolved at all. 

admin.autodiscover()  # Don't know what this function does. 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',                         views.index,             name='index'),
    url(r'^profile/$',                 views.profile,           name='profile'),
    url(r'^pie/$',                     views.pie,               name='piechart'),
    url(r'^line/$',                    views.demo_linechart,    name='linechart'),
    url(r'^scatter/$',                 views.demo_scatterchart, name='scatterchart'),
    url(r'^autograde/(\d+)/(\d+)/$',   views.autograde,         name='autograde'),
    url(r'^item/(\d+)$',               views.item_detail,       name='detail'),
    url(r'^item/$',                    views.items,             name='list'),
    url(r'^table/$',                   views.question_list,     name='question_list'),
    url(r'^question/(\d+)/(\d+)/$',    views.assess_question_detail, name='detail'),
    url(r'^question/(\d+)/$',          views.question_detail,   name='detail'),
    url(r'^question/$',                views.questions,         name='list'),
    url(r'^assessment/(\d+)/$',        views.assessment_detail, name='detail'),
    url(r'^assessment/(\d+)/worksheet/$', views.assessment_worksheet, name='worksheet'),
    url(r'^assessment/$',              views.assessments,       name='list'),
    url(r'^lecture/(\d+)/$',           views.lecture_detail,    name='detail'),
    url(r'^lecture/$',                 views.lectures,          name='list'),
    url(r'^code/(\d+)/$',              views.code_detail,       name='detail'),
    url(r'^login/$',                   views.login_page,        name='login'),
    url(r'^auth/$',                    views.auth,              name='auth'),

]
################################################################################
