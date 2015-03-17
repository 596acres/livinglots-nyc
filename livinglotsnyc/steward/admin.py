from django.contrib import admin

from django_monitor.admin import MonitorAdmin
from livinglots_steward.admin import (StewardNotificationAdminMixin,
                                      StewardProjectAdminMixin)

from autocomplete_light import ModelForm

from .models import StewardNotification, StewardProject


class StewardNotificationAdmin(StewardNotificationAdminMixin, MonitorAdmin):
    pass


class StewardProjectAdminForm(ModelForm):

    class Meta:
        model = StewardProject


class StewardProjectAdmin(StewardProjectAdminMixin, admin.ModelAdmin):
    form = StewardProjectAdminForm


admin.site.register(StewardNotification, StewardNotificationAdmin)
admin.site.register(StewardProject, StewardProjectAdmin)
