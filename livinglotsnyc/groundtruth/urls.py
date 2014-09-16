from django.conf.urls import patterns, url
from django.db.models.signals import post_save

import django_monitor
from django_monitor.util import save_handler

from .models import GroundtruthRecord
from .views import AddGroundtruthRecordView


urlpatterns = patterns('',

    url(r'^add/$', AddGroundtruthRecordView.as_view(),
        name='add_groundtruthrecord'),

)


django_monitor.nq(GroundtruthRecord)


# Disconnect monitor's post-save handler, moderation will be handled in the
# view
post_save.disconnect(save_handler, sender=GroundtruthRecord)
