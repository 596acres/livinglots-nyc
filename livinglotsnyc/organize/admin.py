from django.contrib import admin

from .models import Organizer


class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'type',)
    list_filter = ('type',)
    search_fields = ('name', 'email',)


admin.site.register(Organizer, OrganizerAdmin)
