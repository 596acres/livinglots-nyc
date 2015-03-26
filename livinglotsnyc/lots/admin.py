from django.contrib import admin

import autocomplete_light

from livinglots_lots.admin import BaseLotAdmin

from .models import Lot


class LotAdmin(BaseLotAdmin):
    form = autocomplete_light.modelform_factory(Lot)
    fieldsets = (
            ('NYC specific', {
                'fields': ('bbl',
                           ('borough', 'block', 'lot_number',)),
            }),
        ) + BaseLotAdmin.fieldsets + (
            ('Ownership', {
                'fields': (('owner', 'owner_contact',), 'owner_opt_in',),
            }),
            ('Gutterspace', {
                'fields': ('gutterspace',),
            }),
        )
    list_display = ('pk', 'bbl', 'address_line1', 'borough', 'known_use')
    search_fields = ('bbl', 'address_line1', 'name',)


admin.site.unregister(Lot)
admin.site.register(Lot, LotAdmin)
