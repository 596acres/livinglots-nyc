from django.contrib import admin

from livinglots_organize.admin import BaseOrganizerAdmin

from .models import Organizer


class OrganizerAdmin(BaseOrganizerAdmin):
    pass


admin.site.register(Organizer, OrganizerAdmin)
