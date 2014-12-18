
from django.conf.urls import patterns, url

from articles.views import ArticleList


urlpatterns = patterns('',
    url(r'^$', ArticleList.as_view(), name='faq_index'),
)
