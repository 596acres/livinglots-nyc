from django.contrib import admin

from .models import Organizer


class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'type',)


admin.site.register(Organizer, OrganizerAdmin)
