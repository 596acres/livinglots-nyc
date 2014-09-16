from django.conf.urls import patterns, url

from .views import PathwaysDetailView, PathwaysListView


urlpatterns = patterns('',
    url(r'^$', PathwaysListView.as_view(), name='pathway_list'),
    url(r'^list/$', PathwaysListView.as_view(), name='pathway_list'),

    url(r'^(?P<slug>[^/]+)/$', PathwaysDetailView.as_view(),
        name='pathway_detail'),
)
