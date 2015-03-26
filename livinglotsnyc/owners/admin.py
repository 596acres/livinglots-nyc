from django.contrib import admin

import autocomplete_light

from livinglots_owners.admin import BaseOwnerAdmin, BaseOwnerContactAdmin

from .models import Owner, OwnerContact


class OwnerAdmin(BaseOwnerAdmin):
    form = autocomplete_light.modelform_factory(Owner)


class OwnerContactAdmin(BaseOwnerContactAdmin):
    pass


admin.site.register(Owner, OwnerAdmin)
admin.site.register(OwnerContact, OwnerContactAdmin)
