from django.contrib import admin

import autocomplete_light

from livinglots_owners.admin import BaseOwnerAdmin, BaseOwnerContactAdmin

from .models import Owner, OwnerContact


class OwnerAdmin(BaseOwnerAdmin):
    # NB: setting fields = '__all__', less concerned about security since we 
    # are in the admin site
    form = autocomplete_light.modelform_factory(Owner, fields='__all__')


class OwnerContactAdmin(BaseOwnerContactAdmin):
    pass


admin.site.register(Owner, OwnerAdmin)
admin.site.register(OwnerContact, OwnerContactAdmin)
