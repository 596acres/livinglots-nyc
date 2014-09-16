from django.conf.urls import patterns, url

from .views import ContactFormView

urlpatterns = patterns('',
    url('^$', ContactFormView.as_view(), name='form'),
)
