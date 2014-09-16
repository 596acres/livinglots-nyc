from django.contrib import admin

from django_monitor.admin import MonitorAdmin

from livinglots_groundtruth.admin import GroundtruthRecordAdminMixin

from .models import GroundtruthRecord


class GroundtruthRecordAdmin(GroundtruthRecordAdminMixin, MonitorAdmin):

    def __init__(self, *args, **kwargs):
        super(GroundtruthRecordAdmin, self).__init__(*args, **kwargs)
        self.fields += ('use',)


admin.site.register(GroundtruthRecord, GroundtruthRecordAdmin)
