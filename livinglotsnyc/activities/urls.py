from django.conf.urls import patterns, url

from .views import ActivityListView


urlpatterns = patterns('',

    url(r'^list/', ActivityListView.as_view(), name='activity_list'),

)


from actstream import urls as actstream_urls

urlpatterns += actstream_urls.urlpatterns


from inplace_activity_stream import urls as inplace_activity_stream_urls

urlpatterns += inplace_activity_stream_urls.urlpatterns
