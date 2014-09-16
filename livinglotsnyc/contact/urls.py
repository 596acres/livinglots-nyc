from django.conf.urls import patterns, url

from .views import ContactFormView, ContactCompleted

form_urls = patterns('',
    url('^$', ContactFormView.as_view(), name='form'),
)


success_urls = patterns('',
    url('^success/$', ContactCompleted.as_view(), name='completed'),
)

urlpatterns = form_urls + success_urls
