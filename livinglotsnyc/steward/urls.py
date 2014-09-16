from django.conf.urls import patterns, url
from django.db.models.signals import post_save

import django_monitor
from django_monitor.util import save_handler

from .models import StewardNotification
from .views import AddStewardNotificationView


urlpatterns = patterns('',

    url(r'^add/$', AddStewardNotificationView.as_view(),
        name='add_stewardnotification'),

)


django_monitor.nq(StewardNotification)


# Disconnect monitor's post-save handler--moderation handled in view
post_save.disconnect(save_handler, sender=StewardNotification)
